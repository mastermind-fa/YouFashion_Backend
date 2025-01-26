from django.contrib import admin

from .models import Product, Review, Wishlist

    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'color']
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating']
    
    
admin.site.register(Review, ReviewAdmin)
admin.site.register(Wishlist)



