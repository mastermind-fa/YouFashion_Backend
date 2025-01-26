# products/filters.py
import django_filters
from .models import Product
from .constants import *  # Import SIZE_CHOICES and COLOR_CHOICES

class ProductFilter(django_filters.FilterSet):
    size = django_filters.ChoiceFilter(choices=SIZE_CHOICES)  # Use choices for size
    color = django_filters.ChoiceFilter(choices=COLOR_CHOICES)  # Use choices for color

    class Meta:
        model = Product
        fields = ['size', 'color']