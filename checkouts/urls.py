from django.urls import path
from . import views

urlpatterns = [
    path('sub-price/<int:price_id>/', views.product_price_redirect, name='sub-price-checkout'),
    path('start/', views.checkout_redirect, name='checkout-start'),
    path('success/', views.checkout_finalize, name='checkout-success'),
]