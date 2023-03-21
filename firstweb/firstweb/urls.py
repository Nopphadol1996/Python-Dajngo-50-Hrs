from django.contrib import admin
from django.urls import path,include
# include คือ การลิงค์โปรเจคกับแอพเข้ากัน
# path คือการทำให้เว็บไซต์เรามี  url ย่อย ที่ทำให้เข้าเบื้องหลัง admin ได้

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('myapp.urls')) # บรรทัดนี้เป็นการทำให้โปรเจคลิงค์กับ urls ของแอพ
]
