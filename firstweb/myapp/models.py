from django.db import models


class Allproduct(models.Model): # ภาษาเทคนิคเรียกว่า อินเฮอร์จีเจนท์ models.Model
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True) # blank=True ไม่ต้องกรอกข้อมูลก็ได้ , null=True ในฐานข้อมูลว่างได้
	# ไปรันคำสั่ง python manage.py makemigrations, python manage.py migrate
	imageurl = models.CharField(max_length=200,null=True,blank=True) # EP5
	instock = models.BooleanField(default=True) # EP7 Check ว่ามีสินค้าหรือเปล่า
	quantity = models.IntegerField(default=1) # EP7  ทำจำนวนสินค้า
	unit = models.CharField(max_length=200,default='-')  # EP7  ทำหน่วยของสินค้า
	image = models.ImageField(upload_to="products",null=True,blank=True) # EP7 ทำ upload image form
	# pip install pillow เพื่้อแสดงภาพด้วย

	def __str__(self):
		return self.name
		# ไม่ต้อง migrate เป็นการโชว์ชื่อหลังบ้านจร้า..