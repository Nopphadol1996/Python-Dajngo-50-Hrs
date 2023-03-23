from django.shortcuts import render
from django.http import HttpResponse
# django คือ แพ็คเกจ หลัก .http คือ แพ็คเกจย่อย  HttpResponse คือฟังก์ชั่นที่ทำให้โชว์ข้อความหน้าเว็บได้
from .models import * # EP5
from django.core.files.storage import FileSystemStorage # EP8
from django.contrib.auth.models import User  # EP8 ทำหน้าสมัครสมาชิก
def Home(request):
	# return HttpResponse('สวัสดีชาวโลก...')
	product1 = 'แอปเปิ้ล'
	product2 = 'องุ่น'
	product3 = 'ส้ม'

	context = {'product1':product1,'product2':product2,'product3':product3}
	
	return render(request,'myapp/home.html',context)

def About(request):

	return render(request,'myapp/about.html')

def Contact(request):

	return render(request,'myapp/contact.html')

def Apple(request):

	return render(request,'myapp/apple.html')

# EP5
# from .models import Allproduct
def Addproduct(request):
	# EP8  import FileSystemStorage เพื่อทำ Upload ข้อมูลจากเครื่อง
	if request.method == 'POST' and request.FILES['imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')

		#EP8 รับค่าจาก html
		quantity = data.get('quantity')
		unit = data.get('unit')
		
		# สร้างตัวแปร new  = Allproduct()  Allproduct คือ database เพื่อที่จะบันทึกข้อมูลใหม่ลงไป
		new = Allproduct()
		new.name = name 
		new.price = price
		new.detail = detail
		new.imageurl = imageurl

		# EP 8 save  quantity , unit ลง database
		new.quantity = quantity
		new.unit = unit

		############# EP8 Save Image ##############
		file_image = request.FILES['imageupload']
		file_image_name = request.FILES['imageupload'].name.replace(' ','') # ถ้าชื่อไฟล์มี Spech จะrepalce
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:] # [6:] คือการ slide ข้าม media
		new.save()

	return render(request,'myapp/addproduct.html')

# EP6
def Product(request):
	# product = Allproduct.objects.all() #EP6 ดึงข้อมูลมาจาก Models .objects.all ดึงข้อมูลมาทั้งหมด
	product = Allproduct.objects.all().order_by('id').reverse() # EP7  ดึงข้อมูลล่าสุดไว้ด้านบน
	context = {'product':product}

	return render(request,'myapp/allproduct.html',context)

# EP8 ทำหน้า Register
# from django.contrib.auth.models import User
def Register(request):
	if request.method == 'POST':
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
		newuser.set_password(password)
		newuser.save()

	return render(request,'myapp/register.html')


