from rest_framework import serializers
from .models import Product, Review, Wishlist
from customers.models import Customer
from customers.serializers import CustomerSerializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    def get_size(self, obj):
        return obj.get_size_display()  

    def get_color(self, obj):
        return obj.get_color_display()  
        
    def get_average_rating(self, obj):
        return obj.average_rating()
        

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    
    # user = serializers.StringRelatedField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


class ReviewSerializerGet(serializers.ModelSerializer):
    user = CustomerSerializer()
    
    # user = serializers.StringRelatedField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = ProductSerializer()
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'added_at']
        read_only_fields = ['user', 'added_at']
        
