from django.urls import path
from .views import CartView, CheckoutView, OrderListView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:product_id>/', CartView.as_view(), name='remove-from-cart'),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderListView.as_view(), name='orders'),
]