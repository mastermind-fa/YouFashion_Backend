from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from .constants import *



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    popularity = models.IntegerField(default=0)  
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 2)
        return 0


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()  # 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"
    
    
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlists")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

