from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('audiobook-sl-hl/', views.chapter_resource_view, {'category': 'audiobook_sl_hl'}, name='audiobook_sl_hl'),
    path('audiobook-hl-only/', views.chapter_resource_view, {'category': 'audiobook_hl_only'}, name='audiobook_hl_only'),
    path('audiolibro-nm-ns/', views.chapter_resource_view, {'category': 'audiolibro_nm_ns'}, name='audiolibro_nm_ns'),
    path('audiolibro-ns-solo/', views.chapter_resource_view, {'category': 'audiolibro_ns_solo'}, name='audiolibro_ns_solo'),
    path('notes-and-practice/', views.chapter_resource_view, {'category': 'notes_and_practice'}, name='notes_and_practice'),
    path('notas-y-practica/', views.chapter_resource_view, {'category': 'notas_y_practica'}, name='notas_y_practica'),
    path('subscription/', views.subscription_view, name='subscription'),
    path('subscription/success/', views.subscription_success_view, name='subscription_success'),
    path('shop/', views.shop_view, name='shop'),
    path('shop/success/', views.shop_success_view, name='shop_success'),
]
