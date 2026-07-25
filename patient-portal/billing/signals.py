from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import Inventory


@receiver(post_save, sender=Inventory)
def broadcast_inventory_update(sender, instance, **kwargs):
    """
    Fires every time an Inventory row is saved — including the
    `inv.save(update_fields=['quantity', 'updated_at'])` call inside
    InvoiceCreateSerializer.create(). This is the WebSocket Event
    Broadcast step from your original pipeline diagram.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'inventory_updates',
        {
            'type': 'inventory.update',   # maps to InventoryConsumer.inventory_update()
            'data': {
                'inventory_id': instance.id,
                'medicine_id': instance.medicine_id,
                'medicine_name': instance.medicine.name,
                'pharmacy_id': instance.pharmacy_id,
                'pharmacy_name': instance.pharmacy.name,
                'quantity': instance.quantity,
                'price': str(instance.price),
            },
        }
    )