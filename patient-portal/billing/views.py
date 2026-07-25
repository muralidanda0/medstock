from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import InvoiceCreateSerializer


class InvoiceCreateView(generics.CreateAPIView):
    """
    POST /api/billing/invoices/
    Only pharmacy staff should be allowed to generate bills.
    """
    serializer_class = InvoiceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  # role check refined later

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()
        return Response(
            {'invoice_id': invoice.id, 'total_amount': str(invoice.total_amount)},
            status=201,
        )