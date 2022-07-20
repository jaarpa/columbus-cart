from rest_framework import serializers

from carts.models import CartItem
from inventory.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")
        read_only_fields = ["product"]

    def validate_quantity(self, value):
        """
        Check that the quantity is positive.
        """

        # I could have used a validator here but just to show how to do it
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )
        return value

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.instance.product.stock < validated_data["quantity"]:
            raise serializers.ValidationError("Not enough stock")
        return validated_data
