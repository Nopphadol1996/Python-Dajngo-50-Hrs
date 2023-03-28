from django.contrib import admin
#from .models import Allproduct,Profile # EP4  นำเข้า Class Allproduct ในหน้า models.py
from .models import*

admin.site.site_header = 'Nopphadol fruit amin' #EP15 เปลี่ยนชื่อหน้าแอดมิน
admin.site.index_title = 'Mian Addmin' #EP15 เปลี่ยนชื่อหน้าแอดมิน
admin.site.site_title = 'Nopphadol fruit Blackend' #EP15 เปลี่ยนบนtab

class AllproductAmin(admin.ModelAdmin):
	list_display = ['name','id','instock','price','quantity'] # ทำให้เบื้องหลังโชว์เป็นตาราง
	list_editable = ['instock','price','quantity'] # ทำให้เบื้องหลังแก้ไขได้

admin.site.register(Allproduct,AllproductAmin) #,AllproductAmin
admin.site.register(Profile) #EP9 สร้าง Userprofile
admin.site.register(Cart)

 #EP 15 ทำให้เบื้องหลังโชว์เป็นตาราง
class OrederListAmin(admin.ModelAdmin):
	list_display = ['orderid','productname','total']  # พวกรายการต้องตรงกับใน models นั้นๆ

admin.site.register(OrderList,OrederListAmin) # EP14
admin.site.register(OrderPending) #EP14