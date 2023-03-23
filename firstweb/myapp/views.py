from django.shortcuts import render
from django.http import HttpResponse
# django คือ package หลัก .http คือ packgae ย่อย HttpResponse คือฟังก์ชั่นี่ทำให้โชว์ข้อความหน้าเว็บได้
from .models import Allproduct
from django.core.files.storage import FileSystemStorage #EP8 ทำอัพโหลดไฟล์ผ่านform
from django.contrib.auth.models import User #EP8 ทำหน้าามัครสมาชิก

def Home(request):
	#return HttpResponse('สวัสดีชาวโลก...')

	product1 = 'apple'
	product2 = 'องุ่น.'
	product3 = 'ส้ม.'
	context = {'product1':product1,'product2':product2,'product3':product3}

	return render(request, 'myapp/home.html',context)

def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Apple(request):
	return render(request, 'myapp/apple.html')

	
#from .models import Allproduct # ต้อง import models เข้ามาด้วย EP5 Allproduct ชื่อเดียวกับ โมเดล
# from django.core.files.storage import FileSystemStorage #EP8 ทำอัพโหลดไฟล์ผ่านform
def Addproduct(request):
	if request.method == 'POST' and request.FILES['imageupload']:# ดึงข้อมูลมาจาก form html 
																# and request.FILES['imageupload'] EP8
		data = request.POST.copy() # ถ้ามีการกด submit ให้เก็บไว้ใน ตัวแปร data
		name = data.get('name') # ('name') คือ name="name" ใน html
		price = data.get('price') # ('price') คือ name="price" ใน html
		detail = data.get('detial') # ('detial') คือ name="detial" ใน html
		imageurl = data.get('imageurl') # ('imageurl') คือ name="imageurl" ใน html
		quantity = data.get('quantity')
		unit = data.get('unit')


		new = Allproduct() # สร้างตัว database
		new.name = name # จาก new.name คือ database เราจะให้เท่ากับ name ตัวด้านบน
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		
		######## save image EP8 ###########
		file_image = request.FILES['imageupload']
		file_image_name = request.FILES['imageupload'].name.replace(' ','')
		print('FILES_IMAGE:',file_image)
		print('FILES_IMAGE:',file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:] # ให้ใส่ด้วยเวลา uplode ขึ้น server จะได้ไม่ error ถ้างงกลับมาดู EP8 1:07:00
		########
		new.save()###########
		# เมื่อกด submit จะส่งข้อมูลไปยัง database

	return render(request, 'myapp/addproduct.html')

def Product(request):
	product = Allproduct.objects.all()#.order_by('id').reverse() # ดึงข้อมูลจาก model มาทั้งหมด 
	#.order_by('id').reverse() เอาสิ่งที่บันทึกขึ้่นก่อน
	context = {'product':product}
	return render(request, 'myapp/allproduct.html',context)

#EP8 ทำหน้าามัครสมาชิก
# from django.contrib.auth.models import User
def Register(request):
	if request.method == 'POST':# ดึงข้อมูลมาจาก form html 
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password) # คือตัวแปรด้ายบนจร้า แต่ password ต้องใส่ function set_password(....)
		newuser.save()

	return render(request, 'myapp/register.html')


