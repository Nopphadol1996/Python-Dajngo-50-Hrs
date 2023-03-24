# urls.py
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',Home, name='home-page'),
    path('about/',About, name='about-page'),
    path('contact/',Contact, name='contact-page'),
    path('apple/',Apple, name='apple-page'),
    path('addproduct/',Addproduct, name='addproduct-page'), #EP5
    path('allproduct/',Product, name='allproduct-page'), #EP6
    path('register/',Register, name='register-page'),#EP8 ทำ Register>> localhost:8000/register
    path('addtocart/<int:pid>/',AddtoCart,name='addtocart-page'),# EP10 ทำ ตะกร้าสินค้า
    path('mycart/',MyCart,name='mycart-page'),# EP10

]