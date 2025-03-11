from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('list', views.ProductViewSet)  # For products
# router.register('reviews', views.ReviewListCreateAPIView, basename='review')  # Specify basename
# router.register(r'list/(?P<product_id>\d+)/reviews', views.ReviewListCreateAPIView, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.ProductCreateAPIView.as_view(), name='product-create'),  # POST /products/create/
    path('update/<int:pk>/', views.ProductUpdateAPIView.as_view(), name='product-update'),  # PATCH /products/update/<id>/
    path('delete/<int:pk>/', views.ProductDeleteAPIView.as_view(), name='product-delete'),  # DELETE /products/delete/<id>/

    path('reviews/', views.ReviewListCreateAPIView.as_view(), name='reviews'),
    path('reviews/list/', views.ReviewListGetAPIView.as_view(), name='reviews-list'),
    path('wishlist/', views.WishlistListCreateAPIView.as_view(), name='wishlist-list-create'),
    # path('wishlist/<int:user_id>/', views.WishlistListCreateAPIView.as_view(), name='wishlist'),
    path('wishlist/remove/<int:product_id>/', views.WishlistDeleteAPIView.as_view(), name='wishlist-delete'),
    
]

