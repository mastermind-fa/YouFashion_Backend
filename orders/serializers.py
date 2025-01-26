from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'added_at', 'total_price']