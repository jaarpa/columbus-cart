from decimal import Decimal

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import generics

from core.permissions import IsOwnerOrReadOnly
from core.pagination import StandardResultsSetPagination
from inventory.models import JournalEntry, Product
from inventory.serializers import ProductSerializer, ProductSellerSerializer

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
                seller=self.request.user, available=False
            )
        return products

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

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

        JournalEntry.objects.create(
            user=request.user, product=product, quantity=stock_change
        )

        return Response(self.get_serializer(product).data)

    # @action(methods=['post'], detail=True)
    # def create_materials(self, request, pk=None, *args, **kwargs):
    #     course = self.get_object()
    #     materials = request.data
    # materials = request.data
    # for material in materials:
    #     serializer = MaterialSerializer(
    #         data=material, context={'course': course}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     m = serializer.save()
    #     m.course = course
    #     m.save()
    #
    # def _retrieve(self, instance):
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # @action(methods=['post'], detail=True)
    # def like(self, request, pk=None, *args, **kwargs):
    #     comment = self.get_object()
    #     likes = comment.likes
    #     comment.likes = likes + 1
    #     comment.save()

    #     return self._retrieve(comment)
