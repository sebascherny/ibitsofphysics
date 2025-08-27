from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contacto/', views.contact_view, {'language': 'es'}, name='contacto'),
    path('contact/', views.contact_view, {'language': 'en'}, name='contact'),
    path('audiobook-sl-hl/', views.chapter_resource_view, {'category': 'audiobook_sl_hl', 'language': 'en'}, name='audiobook_sl_hl'),
    path('audiobook-hl-only/', views.chapter_resource_view, {'category': 'audiobook_hl_only', 'language': 'en'}, name='audiobook_hl_only'),
    path('audiolibro-nm-ns/', views.chapter_resource_view, {'category': 'audiolibro_nm_ns', 'language': 'es'}, name='audiolibro_nm_ns'),
    path('audiolibro-ns-solo/', views.chapter_resource_view, {'category': 'audiolibro_ns_solo', 'language': 'es'}, name='audiolibro_ns_solo'),
    path('notes/', views.chapter_resource_view, {'category': 'notes', 'language': 'en'}, name='notes'),
    path('notas/', views.chapter_resource_view, {'category': 'notas', 'language': 'es'}, name='notas'),
    path('practices/', views.chapter_resource_view, {'category': 'practices', 'language': 'en'}, name='practices'),
    path('practicas/', views.chapter_resource_view, {'category': 'practicas', 'language': 'es'}, name='practicas'),
    path('notes-and-practices/', views.chapter_resource_view, {'category': 'notes_and_practices', 'language': 'en'}, name='notes_and_practices'),
    path('notas-y-practicas/', views.chapter_resource_view, {'category': 'notas_y_practicas', 'language': 'es'}, name='notas_y_practicas'),
    path('suscripcion/', views.subscription_view, {'language': 'es'}, name='suscripcion'),
    path('subscription/', views.subscription_view, {'language': 'en'}, name='subscription'),
    path('suscripcion-1-anio/', views.redirect_to_stripe, {'language': 'es', 'type': '1 year'}, name='redirect_to_stripe_1_year_es'),
    path('suscripcion-2-anios/', views.redirect_to_stripe, {'language': 'es', 'type': '2 years'}, name='redirect_to_stripe_2_years_es'),
    path('subscribe-1-year/', views.redirect_to_stripe, {'language': 'en', 'type': '1 year'}, name='redirect_to_stripe_1_year_en'),
    path('subscribe-2-years/', views.redirect_to_stripe, {'language': 'en', 'type': '2 years'}, name='redirect_to_stripe_2_years_en'),
    path('subscribe-early-access/', views.redirect_to_stripe, {'language': 'en', 'type': 'early access'}, name='redirect_to_stripe_promo_en'),
    path('suscripcion-promo/', views.redirect_to_stripe, {'language': 'es', 'type': 'early access'}, name='redirect_to_stripe_promo_es'),

    path('subscription/success/', views.subscription_success_view, {'language': 'en'}, name='subscription_success_en'),
    path('suscripcion/correcta/', views.subscription_success_view, {'language': 'es'}, name='subscription_success_es'),

    path('error-in-payment/', views.error_in_payment_view, {'language': 'en'}, name='error_in_payment_en'),
    path('error-en-pago/', views.error_in_payment_view, {'language': 'es'}, name='error_in_payment_es'),

    path('shop/', views.shop_view, name='shop'),
    path('shop/success/', views.shop_success_view, name='shop_success'),
]
