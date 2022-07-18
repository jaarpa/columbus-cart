from rest_framework import viewsets
from rest_framework import permissions

from inventory.models import Product
from inventory.serializers import ProductSerializer

# Create your views here.


from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    """Custom page number pagination. Allows for custom page size."""

    page_size = 10
    max_page_size = 30
    page_size_query_param = "page_size"


class ProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
