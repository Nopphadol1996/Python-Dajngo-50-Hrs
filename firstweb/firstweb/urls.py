from django.contrib import admin
from django.urls import path,include
# include คือ การลิงค์โปรเจคกับแอพเข้ากัน
# path คือการทำให้เว็บไซต์เรามี  url ย่อย ที่ทำให้เข้าเบื้องหลัง admin ได้


# EP7 สร้าง field ใส่Photo
from . import settings # EP7 ทำ upload image form
from django.contrib.staticfiles.urls import static # EP7 ทำ upload image form
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # EP7 ทำ upload image form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('myapp.urls')) # บรรทัดนี้เป็นการทำให้โปรเจคลิงค์กับ urls ของแอพ
]

# ต้องอยู่ด้านล่าง  urlpatterns = []
urlpatterns += staticfiles_urlpatterns() # EP7 ทำ upload image form
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # EP7 ทำ upload image form