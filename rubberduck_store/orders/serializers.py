from rest_framework import serializers

from orders.models import Order, OrderItem
from inventory.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity")
        read_only_fields = ["product"]


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "orderitem_set",
            "date_placed",
            "estimated_delivery_date",
        )
        read_only_fields = ["orderitem_set"]
