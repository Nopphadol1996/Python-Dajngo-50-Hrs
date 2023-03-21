# urls.py
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',Home, name='home-page'),
    path('about/',About, name='about-page'),
    path('contact/',Contact, name='contact-page'),
    path('apple/',Apple, name='apple-page'),
]