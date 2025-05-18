from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.success_view, name='success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
