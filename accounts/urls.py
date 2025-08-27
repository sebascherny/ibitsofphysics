from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, {'language': 'en'}, name='profile'),
    path('perfil/', views.profile_view, {'language': 'es'}, name='profile'),
]
