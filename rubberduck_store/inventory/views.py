from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework import generics

from core.permissions import IsOwnerOrReadOnly
from core.pagination import StandardResultsSetPagination
from inventory.models import Product
from inventory.serializers import ProductSerializer, ProductSellerSerializer

# Create your views here.


class ProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited depends on user permissions.
    """

    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
        IsOwnerOrReadOnly,
    ]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

    def get_serializer_class(self):
        buyer_serializer = super().get_queryset()
        if self.request.user.groups.filter(name="Sellers").exists():
            return ProductSellerSerializer
        return buyer_serializer

    def get_queryset(self):
        products = super().get_queryset()
        if self.request.user.groups.filter(name="Sellers").exists():
            products |= Product.objects.filter(
                seller=self.request.user, available=False
            )
        return products

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
