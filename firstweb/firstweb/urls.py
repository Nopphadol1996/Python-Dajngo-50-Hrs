from django.contrib import admin
from django.urls import path,include

from . import settings # EP7 ทำ upload image form
from django.contrib.staticfiles.urls import static # EP7 ทำ upload image form
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # EP7 ทำ upload image form

from django.contrib.auth import views as authen_views # EP9 หน้า LOGIN


# include คือ การลิงค์โปรเจคกับแอพเข้ากัน
# path คือ การทำให้เว็บไวต์เรามี url ย่อย ที่ทำให้เข้า เบื้องหลัง admin ได้
urlpatterns = [
    path('admin/', admin.site.urls), #localhost:8000/admin
    path('',include('myapp.urls')), #localhost:8000
    # บรรทัดนี้ทำให้โปรเจคลิงค์กับ urls ของแอพ
    path('login/', authen_views.LoginView.as_view(template_name='myapp/login.html'),name='login'),
    path('logout/', authen_views.LogoutView.as_view(template_name='myapp/logout.html'),name='logout'),

]

# ต้องอยู่ด้านล่าง  urlpatterns = []
urlpatterns += staticfiles_urlpatterns() # EP7 ทำ upload image form
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # EP7 ทำ upload image form
