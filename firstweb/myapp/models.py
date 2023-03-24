from django.db import models
from django.contrib.auth.models import User

#EP 9 ทำโปรไฟล์ให้กับ User
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	photo = models.ImageField(upload_to="photoprofile",null=True,blank=True,default='defaultprofile.png')
	usertype = models.CharField(max_length=100,default='member')

	def __str__(self):
		return self.user.first_name

# ถ้ามีการเปลี่ยนแปลงข้อมูลต้อง run 2 คำสั่งนี้เสมอ
# python manage.py makemigrations
# python manage.py migrate

class Allproduct(models.Model): # EP4
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True) # null=True blank=True ในฐานข้อมูลว่างได้ ไม่ต้องกรอก

	#EP5 
	imageurl = models.CharField(max_length=200,null=True,blank=True)
	# EP7
	instock = models.BooleanField(default=True) # EP7เช็คสินค้า
	quantity = models.IntegerField(default=1) # EP7 จำนวนสินค้า
	unit = models.CharField(max_length=200,default='-') # หน่วยสินค้า ถ้า user ไม่กรอกจะกำหนดค่า default
	image = models.ImageField(upload_to="products",null=True,blank=True)# EP7 สร้าง field ใส่Photo 
	
	# EP4 ทำให้เบื้องหลังเห็นชื่อ
	def __str__(self):
		return self.name

# EP10 ทำตระกร้าสินค้า
class Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	productid = models.CharField(max_length=100)
	productname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		
		return self.productname
