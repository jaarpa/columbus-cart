from rest_framework import serializers

from carts.models import CartItem
from inventory.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")
        read_only_fields = ["product"]

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data["product"].stock < validated_data["quantity"]:
            raise serializers.ValidationError("Not enough stock")
        return validated_data
