from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)  # True when the order is placed

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity