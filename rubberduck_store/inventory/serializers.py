from rest_framework import serializers

from inventory.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSellerSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["available"]
        extra_kwargs = {
            "seller": {"required": False},
            "productimage_set": {"required": False},
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "seller",
            "description",
            "price",
            "productimage_set",
        ]
        read_only_fields = [
            "name",
            "seller",
            "description",
            "price",
            "productimage_set",
        ]
