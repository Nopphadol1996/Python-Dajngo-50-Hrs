from django.db import models
from django.contrib.auth.models import User

#EP 9 ทำโปรไฟล์ให้กับ User
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	photo = models.ImageField(upload_to="photoprofile",null=True,blank=True,default='defaultprofile.png')
	usertype = models.CharField(max_length=100,default='member')
	#EP11 
	cartquan = models.IntegerField(default=0) # ใช้เก็บจำนวนสินค้าในตะกร้าว่ามีกี่ชิ้น

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


# EP14 สร้าง Orderlist
class OrderList(models.Model):
	orderid = models.CharField(max_length=100)
	productid = models.CharField(max_length=100) # productid ณ เวลาตอนนั้น
	productname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()

# EP14 สร้าง OrderPending เก็บ รายละเอียดของ orderlist
class OrderPending(models.Model):
	orderid = models.CharField(max_length=100)
	user = models.ForeignKey(User,on_delete=models.CASCADE) # User ไหนเป็นคนสั่ง
	name = models.CharField(max_length=100) # ชื่อที่อยู่ผู้รับ
	tel = models.CharField(max_length=100)  # เบอร์ผู้รับ
	address = models.TextField()
	shipping = models.CharField(max_length=100) # EMS
	payment = models.CharField(max_length=100)  # โอนเงิน พร้อมเพย์ , ธนาคารอะไร
	other = models.TextField(null=True,blank=True) # หมายเหตุของผู้รับ ต้องใส่ blank=True ด้วย
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True) # ออร์เดอร์ stamp วันไหน 
	paid = models.BooleanField(default=False) # เช็ตสถานะจ่ายเงินแล้วหรือยัง
	slip = models.ImageField(upload_to="slip",null=True,blank=True) # อัพโหลด slip แล้วหรือยัง
	sliptime = models.CharField(max_length=100,null=True,blank=True) # มาเพิ่มเป็นประเภท datetime  พร้อมกับ calendar html EP15
	paymentid = models.CharField(max_length=100,null=True,blank=True) #เก็บไว้ยังไม่ใช้
	trackingnumber = models.CharField(max_length=100,null=True,blank=True) # EP17 ส่งเลข พัสดุ

	def __str__(self):
		return self.name


