from rest_framework import serializers

from carts.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data["product"].get_stock() < validated_data["quantity"]:
            raise serializers.ValidationError("Not enough stock")
        return validated_data
