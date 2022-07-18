from rest_framework import serializers

from inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "seller",
            "description",
            "available",
            "price",
            "seller_price",
            "productimage_set",
        ]
        read_only_fields = ["productimage_set"]
