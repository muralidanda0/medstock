from rest_framework import serializers
from django.db import transaction
from inventory.models import Inventory
from .models import Invoice, InvoiceItem
from decimal import Decimal


class InvoiceItemInputSerializer(serializers.Serializer):
    """
    What the pharmacist's billing screen sends us for EACH item in the cart.
    Just inventory_item id + quantity — everything else (price, name) we
    fetch ourselves from the database, never trust the client for price.
    """
    inventory_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class InvoiceCreateSerializer(serializers.Serializer):
    """
    Handles the full "generate bill" transaction described in your spec:
    Billing Software -> Invoice Generated -> Inventory Reduced -> ...
    """
    pharmacy_id = serializers.IntegerField()
    customer_name = serializers.CharField(required=False, allow_blank=True)
    customer_phone = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=Invoice.PaymentMethod.choices)
    items = InvoiceItemInputSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("An invoice must have at least one item.")
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = self.context['request']

        # WHY select_for_update: without it, two pharmacists billing the
        # SAME medicine at the SAME moment (race condition) could both read
        # "10 units available" and both proceed, overselling stock. This
        # locks the row until the transaction commits, forcing the second
        # request to wait and re-check against the updated quantity.
        with transaction.atomic():
            inventory_map = {}
            for item in items_data:
                inv = Inventory.objects.select_for_update().get(
                    id=item['inventory_item_id']
                )
                if inv.quantity < item['quantity']:
                    raise serializers.ValidationError(
                        f"Insufficient stock for {inv.medicine.name}: "
                        f"requested {item['quantity']}, available {inv.quantity}"
                    )
                inventory_map[item['inventory_item_id']] = inv

            invoice = Invoice.objects.create(
                pharmacy_id=validated_data['pharmacy_id'],
                customer_name=validated_data.get('customer_name', ''),
                customer_phone=validated_data.get('customer_phone', ''),
                payment_method=validated_data['payment_method'],
                created_by=request.user,
            )

            subtotal = 0
            for item in items_data:
                inv = inventory_map[item['inventory_item_id']]
                InvoiceItem.objects.create(
                    invoice=invoice,
                    inventory_item=inv,
                    medicine_name=inv.medicine.name,   # snapshot at sale time
                    unit_price=inv.price,              # snapshot at sale time
                    quantity=item['quantity'],
                )
                subtotal += inv.price * item['quantity']

                # THE CORE SYNC STEP from your spec: Invoice Items Stored -> Inventory Reduced
                inv.quantity -= item['quantity']
                inv.save(update_fields=['quantity', 'updated_at'])

            gst = subtotal * Decimal('0.05')  # simplified flat 5% GST for MVP
            invoice.subtotal = subtotal
            invoice.gst_amount = gst
            invoice.total_amount = subtotal + gst - invoice.discount
            invoice.save()

            # Next step in the pipeline (Redis cache clear + WebSocket
            # broadcast) will be added when we build the realtime app —
            # we'll hook it in here via a signal, so billing logic itself
            # stays clean and doesn't need to know about WebSockets.

        return invoice