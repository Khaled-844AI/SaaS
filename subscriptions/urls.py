from django.urls import path
from . import views
urlpatterns = [
    path('pricing/',views.subscription_pricing_view, name='pricing'),
    path('pricing/<str:interval>',views.subscription_pricing_view, name='pricing_interval'),
]