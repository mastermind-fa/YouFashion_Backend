from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from sslcommerz_lib import SSLCOMMERZ
from orders.models import Order, Cart
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import uuid
from rest_framework import status  # Make sure this import is at the top of your file
from django.conf import settings
from django.shortcuts import redirect
from customers.models import Customer

class PaymentViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price
        total_price = sum(item.total_price for item in cart_items)
        
        
        # SSLCommerz configuration
        sslcz_settings = {
            'store_id': 'maste679cfa8ec592d',
            'store_pass': 'maste679cfa8ec592d@ssl',
            'issandbox': True
        }
        sslcz = SSLCOMMERZ(sslcz_settings)
        
        # Generate unique transaction ID
        tran_id = str(uuid.uuid4())[:10].replace('-', '').upper()
        
        # Extract and set default request data
        user_id = request.user.id
        
        
        # Define callback URLs
        success_url = request.build_absolute_uri(f'/payment/success/')
        # fail_url = request.build_absolute_uri(f'/payment/cancel/')
        fail_url = request.build_absolute_uri('/payment/fail/')
        cancel_url = request.build_absolute_uri('/payment/cancel/')

        # Create payment information payload
        post_body = {
            'total_amount': total_price,
            'currency': "BDT",
            'tran_id': tran_id,  # Unique transaction ID
            'success_url': success_url,
            'fail_url': fail_url,
            'cancel_url': cancel_url,
            'emi_option': "0",
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_phone': "123456789",  # Replace with user's phone number if available
            'cus_add1': "N/A",
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': len(cart_items),
            'product_name': "Fashion Products",
            'product_category': "Fashion",
            'product_profile': "general",
        }

        try:
            user=User.objects.get(id=user_id)
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items.exists():
                return Response({"error": "No active cart items found for the user."}, status=status.HTTP_404_NOT_FOUND)
            
            print(request.user)
            for item in cart_items:
                print(item)
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity
                )
                item.delete()
            response = sslcz.createSession(post_body)
            if response.get('status') == 'SUCCESS' and 'GatewayPageURL' in response:
                return Response({"url": response['GatewayPageURL']})
            return Response({"error": "Unable to create payment session"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])    
    def success(self, request):
        
        try:
            
            print("Hello")
            
            #print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
            #print(f"Auth headers: {request.headers}")
                
            # cart_items = Cart.objects.filter(user=request.user)
            # print(request.user)
            # for item in cart_items:
            #     print(item)
            #     Order.objects.create(
            #         user=request.user,
            #         product=item.product,
            #         quantity=item.quantity
            #     )
            #     item.delete()

            
            

            return redirect(settings.SUCCESS_URL)

        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        return redirect(settings.CANCEL_URL)
    
    @action(detail=False, methods=['post'])
    def fail(self, request):
        return redirect(settings.FAIL_URL)
