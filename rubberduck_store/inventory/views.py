from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from inventory.models import Product
from inventory.serializers import ProductSerializer, ProductSellerSerializer
from inventory.pagination import StandardResultsSetPagination

# Create your views here.


class ProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited depends on user permissions.
    """

    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    queryset = Product.objects.filter(available=True)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name="Sellers").exists():
            return ProductSellerSerializer
        return ProductSerializer

    def get_queryset(self):
        products = Product.objects.filter(available=True)
        if self.request.user.groups.filter(name="Sellers").exists():
            products |= Product.objects.filter(
                seller=self.request.user, available=False
            )
        return products

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)
