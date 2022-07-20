from rest_framework import viewsets, permissions

from core.pagination import StandardResultsSetPagination
from carts.models import CartItem
from carts.serializers import CartItemSerializer

# Create your views here.


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited depends on user permissions.
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = CartItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        current_user = self.request.user
        cart_items = CartItem.objects.filter(owner=current_user)
        return cart_items
