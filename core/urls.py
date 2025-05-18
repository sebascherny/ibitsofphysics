from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about-the-author/', views.about_view, name='about_the_author'),
    path('teacher-notes/', views.teacher_notes_view, name='teacher_notes'),
    path('contact/', views.contact_view, name='contact'),
    path('miscellaneous/', views.miscellaneous_view, name='miscellaneous'),
    path('specimen-papers/', views.specimen_papers_view, name='specimen_papers'),
]
