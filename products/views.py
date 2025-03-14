from django.shortcuts import render
from .models import Product, Review
from .filters import ProductFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import ProductSerializer, ReviewSerializer, ReviewSerializerGet
from rest_framework import permissions

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'popularity']
    search_fields = ['name']
  
class ProductCreateAPIView(APIView):
    # permission_classes = [IsAdminUser]  # Only admins can create products

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateAPIView(APIView):
    # permission_classes = [IsAdminUser]  # Only admins can update products

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(APIView):
    # permission_classes = [IsAdminUser]  # Only admins can delete products

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
  
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

class ReviewListCreateAPIView(APIView):
    

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically assign the user who is creating the review
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ReviewListGetAPIView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        product_id = request.query_params.get('product', None)
        if product_id:
            reviews = Review.objects.filter(product_id=product_id)
        else:
            reviews = Review.objects.all().order_by('-created_at')

        serializer = ReviewSerializerGet(reviews, many=True)
        return Response(serializer.data)

    
 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist, Product
from .serializers import WishlistSerializer

class WishlistListCreateAPIView(APIView):
    #permission_classes = [IsAuthenticated]  

    def get(self, request):
        
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        
        product = request.data.get('product')
        if not product:
            return Response({"detail": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        
        if Wishlist.objects.filter(user=request.user, product=product).exists():
            return Response({"detail": "Product already in wishlist."}, status=status.HTTP_400_BAD_REQUEST)

        
        wishlist_item = Wishlist.objects.create(user=request.user, product=product)
        serializer = WishlistSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class WishlistDeleteAPIView(APIView):
    #permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def delete(self, request, product_id):
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
        except Wishlist.DoesNotExist:
            return Response({"detail": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)

        # Remove the product from the wishlist
        wishlist_item.delete()
        return Response({"detail": "Product removed from wishlist."}, status=status.HTTP_204_NO_CONTENT)
    

    

