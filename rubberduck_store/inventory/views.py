from decimal import Decimal

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.permissions import IsOwnerOrReadOnly
from core.pagination import StandardResultsSetPagination
from inventory.models import JournalEntry, Product
from inventory.serializers import ProductSerializer, ProductSellerSerializer
from carts.models import CartItem

# Create your views here.


class ProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited depends on user permissions.
    """

    permission_classes = [
        IsOwnerOrReadOnly,
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

    def get_serializer_class(self):
        buyer_serializer = super().get_serializer_class()
        if self.request.user.groups.filter(name="Sellers").exists():
            return ProductSellerSerializer
        return buyer_serializer

    def get_queryset(self):
        products = super().get_queryset()
        if self.request.user.groups.filter(name="Sellers").exists():
            products |= Product.objects.filter(
                owner=self.request.user, available=False
            )
        return products

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=["post"], detail=True)
    def add_stock(self, request, *args, **kwargs):
        product = self.get_object()
        try:
            stock_change = Decimal(request.data.get("stock", "0"))
        except Exception:
            return Response(
                {"error": "Invalid stock change"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product_stock = product.stock
        if product_stock + stock_change < 0:
            return Response(
                {
                    "error": f"{product_stock} + ({stock_change}) results in negative stock"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        JournalEntry.objects.create(
            owner=request.user, product=product, quantity=stock_change
        )

        return Response(self.get_serializer(product).data)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_cart(self, request, pk=None):
        product = self.get_object()
        stock = product.stock
        if stock <= 0:
            return Response(
                {"error": "Product has not enough stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cartitem, created = CartItem.objects.get_or_create(
            owner=request.user, product=self.get_object()
        )
        if not created:
            if cartitem.quantity + 1 > stock:
                return Response(
                    {"error": "Product has not enough stock"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cartitem.quantity += 1
            cartitem.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
