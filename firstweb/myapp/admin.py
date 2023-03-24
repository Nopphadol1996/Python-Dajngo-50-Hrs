from django.contrib import admin
from .models import Allproduct,Profile # EP4  นำเข้า Class Allproduct ในหน้า models.py

admin.site.register(Allproduct)
admin.site.register(Profile) #EP9 สร้าง Userprofile
