from rest_framework import serializers
from .models import Cart, Order
from products.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'added_at', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID

    class Meta:
        model = Order
        fields = ['id', 'product', 'user', 'quantity', 'ordered_at', 'total_price']