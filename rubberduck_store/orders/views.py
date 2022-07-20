from rest_framework import viewsets, permissions

from core.permissions import IsSeller
from core.pagination import StandardResultsSetPagination
from orders.serializers import OrderSerializer, OrderItemSerializer
from orders.models import Order, OrderItem


# Create your views here.
class OrderViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        current_user = self.request.user
        orders = Order.objects.filter(owner=current_user)
        return orders


class SalesViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSeller]
    serializer_class = OrderItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        current_user = self.request.user
        order_items = OrderItem.objects.filter(
            journal_entry__product__owner=current_user
        )
        return order_items
