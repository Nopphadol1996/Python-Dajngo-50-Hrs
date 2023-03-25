from django.shortcuts import render,redirect #EP9 redirect
from django.http import HttpResponse
# django คือ แพ็คเกจ หลัก .http คือ แพ็คเกจย่อย  HttpResponse คือฟังก์ชั่นที่ทำให้โชว์ข้อความหน้าเว็บได้
# from .models import Allproduct,Profile # EP9 Profile
from .models import * # EP5 import *  คือไม่ต้องพิมพ์ Allproduct,Profile
from django.core.files.storage import FileSystemStorage # EP8
from django.contrib.auth.models import User  # EP8 ทำหน้าสมัครสมาชิก
from django.contrib.auth import authenticate ,login # EP9 Login Auto

def Home(request):
	# return HttpResponse('สวัสดีชาวโลก...')
	product = Allproduct.objects.all().order_by('id').reverse()[:3]
	# EP10 quantity__lte =0 (หาที่ quantity <=0)    (underscore 2 ตัว)
	# EP10 quantity__gt = 0 (หาที่ quantity > 0)
	# EP10 quantity__gte = 5 (หาที่ quantity >= )
	preorder = Allproduct.objects.filter(quantity__lte=0) # EP10 quantity__lte
	context = {'product':product,'preorder':preorder}

	return render(request,'myapp/home.html',context)

def About(request):

	return render(request,'myapp/about.html')

def Contact(request):

	return render(request,'myapp/contact.html')

def Apple(request):

	return render(request,'myapp/apple.html')

# EP5
# from .models import Allproduct
# from django.shortcuts import render,redirect #EP9 redirect
def Addproduct(request):

	# EP9 redirect ถ้าไม่ใช่ admin ให้กลับไปที่หน้า home-page
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
		
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

		# EP9 AUtoLogin
		# from .models import Allproduct,Profile # import  Profile ด้วย
		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()
		# from django.contrib.auth import authenticate ,login # EP9 Login Auto
		user = authenticate(username=email,password=password)
		login(request,user)

	return render(request,'myapp/register.html')

#EP10 ตะกร้าสินค้า
def AddtoCart(request,pid):
	# localhost:8000/addtocart/3    3 คือ pid
	# {% url 'addtocart-page' pd.id %}
	print('CRUENT USER',request.user)
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid) # เช็คประเภทของสินค้า

	# EP11 ถ้าซื้อสินค้าชนิดเดียวกันจะให้รวมกัน
	try:
		# กรณีสินค้ามีซ้ำ
		newcart = Cart.objects.get(user=user,productid=str(pid))
		#print('EXISTS:',pcheck.exists())
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = int(check.price) * newquan
		newcart.total = calculate
		newcart.save()

		# Update จำนวนของตะกร้าสินค้า ณ ตอนนี้
		#EP10 ไปสร้าง cartquan = models.IntegerField(default=0) # ใช้เก็บจำนวนสินค้าในตะกร้าว่ามีกี่ชิ้น
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count]) # สั่ง sum forloop แบบบรรทัดเดียว
		updatequan = Profile.objects.get(user=user) # Update databaseของ profile
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')

	except:
		#EP10 ทำตะกร้าสินค้า
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price) # ใน model เป็น Char ใน All product
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()

		# Update จำนวนของตะกร้าสินค้า ณ ตอนนี้
		#EP10 ไปสร้าง cartquan = models.IntegerField(default=0) # ใช้เก็บจำนวนสินค้าในตะกร้าว่ามีกี่ชิ้น
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count]) # สั่ง sum forloop แบบบรรทัดเดียว
		updatequan = Profile.objects.get(user=user) # Update databaseของ profile
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')

# EP10 ฟังก์ชั่นหน้า mycart
def MyCart(request):
	#EP10
	username = request.user.username
	user = User.objects.get(username=username)

	#EP11 ทำ alert
	context = {}

	#EP11 ใช้ สำหรับการลบเท่านั้น
	if request.method == 'POST':
		data = request.POST.copy()
		productid = data.get('productid')
		item = Cart.objects.get(user=user,productid=productid)
		item.delete()
		#EP11 ทำ Alert
		context['status'] = 'delete' #EP11 ทำ Alert

		# EP11 Update จำนวนของตะกร้าสินค้า ณ ตอนนี้ เมื่อทำการลบแล้ว

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count]) # สั่ง sum forloop แบบบรรทัดเดียว
		updatequan = Profile.objects.get(user=user) # Update databaseของ profile
		updatequan.cartquan = count
		updatequan.save()

	#EP10
	mycart = Cart.objects.filter(user=user)
	context['mycart'] = mycart #EP11 ทำ Alert

	return render(request,'myapp/mycart.html',context)



