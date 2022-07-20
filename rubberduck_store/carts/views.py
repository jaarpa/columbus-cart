from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from core.pagination import StandardResultsSetPagination
from carts.models import CartItem
from carts.serializers import CartItemSerializer
from orders.models import Order, OrderItem
from inventory.models import JournalEntry

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

    @action(methods=["post"], detail=False)
    def pay(self, request):
        cartitems = self.get_queryset()

        if not cartitems.exists():
            return Response(
                {"pay": "No items in cart"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check that items are still available
        unavailable_items = []
        for item in cartitems:
            if item.product.stock < item.quantity:
                unavailable_items.append(item)
        if unavailable_items:
            return Response(
                self.get_serializer(unavailable_items, many=True).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Create order
        order = Order(owner=request.user)
        order.save()

        # Add items to the order and create the journal entries
        journal_entries = JournalEntry.objects.bulk_create(
            [
                JournalEntry(
                    owner=request.user,
                    product=item.product,
                    quantity=-item.quantity,
                )
                for item in cartitems
            ]
        )
        orderitems = [
            OrderItem(order=order, journal_entry=journal_entry)
            for journal_entry in journal_entries
        ]
        OrderItem.objects.bulk_create(orderitems)

        # Clear cart
        cartitems.delete()

        return Response(
            status=status.HTTP_202_ACCEPTED,
        )
