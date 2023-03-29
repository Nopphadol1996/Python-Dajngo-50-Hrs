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
    path('mycart/edit/',MyCartEdit,name='mycartedit-page'),# EP11 แก้ไขข้อมูลใน Mycart
    path('checkout/',Checkout,name='checkout-page'), #EP13 Checkout
    path('orderlist/',OrderListPage,name='orderlist-page'),#EP15 OrderList
    path('allorderlist/',AllOrderListPage,name='allorderlist-page'),#EP15 OrderList สำหรับแอดมินดู
    path('uploadslip/<str:orderid>/',UploadSlip,name='uploadslip-page'), # EP16 orderid ต้องตรงกับ parameter ของ function
]