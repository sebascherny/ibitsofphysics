from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, {'language': 'en'}, name='profile'),
    path('perfil/', views.profile_view, {'language': 'es'}, name='profile'),
    # Password change (EN/ES)
    path('password/change/', views.PasswordChangeViewEn.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDoneEn.as_view(), name='password_change_done'),
    path('contrasena/cambiar/', views.PasswordChangeViewEs.as_view(), name='password_change_es'),
    path('contrasena/cambiar/listo/', views.PasswordChangeDoneEs.as_view(), name='password_change_done_es'),
]
