# urls.py
from django.urls import path,include
#from .views import Home , About , Contact , Apple, Addproduct,Product
# EP3 : About , Contact ต้องเหมือนกับตัว functionที่ อยู่ใน views.py Addproduct EP5,Allproduct EP6
from .views import *

urlpatterns = [
    path('', Home, name='home-page'), # ใส่ชื่อเล่นเพื่อจะไปใช้ใน html เวลกดจะให้ไปหน้าไหน EP3
    path('about/',About, name='about-page'),
    path('contact/',Contact, name='contact-page'),
    path('apple/',Apple, name='apple-page'),
    path('addproduct/',Addproduct, name='addproduct-page'),
    path('allproduct/',Product, name='allproduct-page'),
    path('register/',Register, name='register-page'),
]

