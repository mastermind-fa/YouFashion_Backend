from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

class CartView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        
        cart_items = Order.objects.filter(user=request.user, is_ordered=False)
        serializer = OrderSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        
        order, created = Order.objects.get_or_create(
            user=request.user,
            product=product,
            is_ordered=False,
            defaults={'quantity': quantity}
        )

        if not created:
            order.quantity += quantity
            order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        
        try:
            order = Order.objects.get(user=request.user, product_id=product_id, is_ordered=False)
            order.delete()
            return Response({"message": "Product removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)

class CheckoutView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        # Mark all cart items as ordered
        cart_items = Order.objects.filter(user=request.user, is_ordered=False)
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            item.is_ordered = True
            item.save()

        return Response({"message": "Order placed successfully."}, status=status.HTTP_200_OK)
    
    
class OrderListView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all orders for the authenticated user that are marked as ordered
        orders = Order.objects.filter(user=request.user, is_ordered=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)