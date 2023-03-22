from django.db import models

# ถ้ามีการเปลี่ยนแปลงข้อมูลต้อง run 2 คำสั่งนี้เสมอ
# python manage.py makemigrations
# python manage.py migrate

class Allproduct(models.Model): # EP4
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True) # null=True blank=True ในฐานข้อมูลว่างได้ ไม่ต้องกรอก

	#EP5 
	imageurl = models.CharField(max_length=200,null=True,blank=True)
	


	# EP4 ทำให้เบื้องหลังเห็นชื่อ
	def __str__(self):
		return self.name


