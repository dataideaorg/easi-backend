from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_form, name='contact_form'),
    path('newsletter/', views.newsletter_form, name='newsletter_form'),
] 