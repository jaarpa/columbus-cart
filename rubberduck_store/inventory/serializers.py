from rest_framework import serializers

from inventory.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSellerSerializer(serializers.ModelSerializer):
    stock = serializers.DecimalField(
        read_only=True, max_digits=8, decimal_places=2
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "owner",
            "description",
            "available",
            "price",
            "seller_price",
            "productimage_set",
            "stock",
        ]
        read_only_fields = ["available"]
        extra_kwargs = {
            "owner": {"required": False},
            "productimage_set": {"required": False},
        }


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.DecimalField(
        read_only=True, max_digits=8, decimal_places=2
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "owner",
            "description",
            "price",
            "productimage_set",
            "stock",
        ]
        read_only_fields = [
            "name",
            "owner",
            "description",
            "price",
            "productimage_set",
        ]
        read_only_fields = ["owner"]
