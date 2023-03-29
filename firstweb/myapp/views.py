from django.shortcuts import render,redirect #EP9 redirect
from django.http import HttpResponse
# django คือ แพ็คเกจ หลัก .http คือ แพ็คเกจย่อย  HttpResponse คือฟังก์ชั่นที่ทำให้โชว์ข้อความหน้าเว็บได้
# from .models import Allproduct,Profile # EP9 Profile
from .models import * # EP5 import *  คือไม่ต้องพิมพ์ Allproduct,Profile
from django.core.files.storage import FileSystemStorage # EP8
from django.contrib.auth.models import User  # EP8 ทำหน้าสมัครสมาชิก
from django.contrib.auth import authenticate ,login # EP9 Login Auto
from datetime import datetime


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
	# print('CRUENT USER',request.user)
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid) # เช็คประเภทของสินค้า

	# EP11 ถ้าซื้อสินค้าชนิดเดียวกันจะให้รวมกัน
	try:
		# กรณีสินค้ามีซ้ำ
		newcart = Cart.objects.get(user=user,productid=pid)
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
		#EP11 ไปสร้าง cartquan = models.IntegerField(default=0) # ใช้เก็บจำนวนสินค้าในตะกร้าว่ามีกี่ชิ้น
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

	count = sum([ c.quantity for c in mycart]) # EP12 sum qualtity เพื่อไปแสดงผลรวม
	total = sum([ c.total for c in mycart]) # EP12 sum total เพื่อไปแสดงผลรวม

	context['mycart'] = mycart #EP11 ทำ Alert
	context['count'] = count # EP12 แนบ context ไปหน้า html แสดงจำนวน
	context['total'] = total # EP12 แนบ context ไปหน้า html แสดงราคา

	return render(request,'myapp/mycart.html',context)

# EP12  mycart_EDIT ไปสร้างหน้า hrml ด้วย
def MyCartEdit(request):
	# EP11
	username = request.user.username # เช็คว่า userไหนล็อกอิน
	user = User.objects.get(username=username)

	#EP11 ทำ alert
	context = {}

	#EP12 แก้ไขจำนวนสินค้า
	if request.method == 'POST':
		data = request.POST.copy()
		#print(data) # ข้อมูลที่ได้มาเป็น qureydic

		### EP12 จะทำการลบสินค้าในหน้าแก้ไข
		if data.get('clear') == 'clear':
			# print(data.get('clear'))
			Cart.objects.filter(user=user).delete()
			# update profile
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0 
			updatequan.save()
			return redirect('mycart-page')

		# EP12 แก้ไขจำนวนสินค้า
		editlist = []
		for k ,v in data.items(): # k = key  v = value
			# print([k,v])
			# <td><input type="text" name="pd_{{pd.productid}}" value="{{pd.quantity}}"></td>
			if k[:2] == 'pd':  #pd มาจาก name  ,,,  เช็คว่า k[:2] น้อยกว่า2 ใช่ pd หรือเปล่า
				pid = int(k.split('_')[1]) # ตัดคำที่ _ [1] คือเลือกตัวสุดท้าย
				dt = [pid,int(v)]
				editlist.append(dt)
		print('EDITLIST: ',editlist) #[[9,10],[7,8]] 9 = productid ,10 =quantity

		for ed in editlist:
			# print('productid= ',ed[0])
			# print('quan= ',ed[1])
			edit = Cart.objects.get(productid=ed[0],user=user)
		# productid ,,, user=user คือเฉพาะแค่ userนั้นที่ทำการสั่งซื้อ ถ้าไม่ไส่ ,user=user จะลบทุก user ที่ซื้อชิ้นเดียวกัน
			edit.quantity = ed[1] #quantity ใหม่ ที่จะไป update
			calculate = edit.price * ed[1] # คำนวนราคาใหม่เมื่อมีการเปลี่ยนข้อมูล
			edit.total = calculate
			edit.save()

		# update profile
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('mycart-page')

	mycart = Cart.objects.filter(user=user)
	context['mycart'] = mycart #EP11 ทำ Alert

	return render(request,'myapp/mycartedit.html',context)

#EP13 ทำเช็ค CHECKOUT
def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)

	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')

		#ส่งข้อมูลไปยัง checkout2 เพื่อกรอกข้อมูลการจัดส่ง 
		if page == 'information': # ถ้ามีการกดปุ่ม Next ส่งข้อมูลไปยัง checkout2
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			# ดึงข้อมูลจาก database มา show ใน table ว่าสินค้ามีอะไรบ้างลูกค้าสั่ง หน้า checkout2
			mycart = Cart.objects.filter(user=user) 
			count = sum([ c.quantity for c in mycart]) # EP12 sum qualtity เพื่อไปแสดงผลรวม
			total = sum([ c.total for c in mycart]) # EP12 sum total เพื่อไปแสดงผลรวม

			context['mycart'] = mycart #EP11 ทำ Alert
			context['count'] = count # EP12 แนบ context ไปหน้า html แสดงจำนวน
			context['total'] = total # EP12 แนบ context ไปหน้า html แสดงราคา

			return render(request, 'myapp/checkout2.html',context)
		# EP13	
		if page == 'confirm':
			print('Confirm')
			print(data)

			# EP 14 ต่อๆ 
			mycart = Cart.objects.filter(user=user)

			# id =   Order id ไม่ควรจะเริ่มต้นด้วย 0 เพราะ db บางตัวอาจจะไม่นำมาคิด

			# id = OD0007 202 09 03 22 00 30
			# id = OD 0230 2020 09 03 22 00 30
			# from datetime import datetime
			mid = str(user.id).zfill(4) # zfill คือ การเติม 0 ด้านหน้า ไม่สามารถใช้กับ Integerได้ ต้องแปลงเป็น str ก่อน
			dt = datetime.now().strftime('%Y%m%d%H%M%S') # ทำหรัสจากวันที่เพื่อจะได้ไม่ให้ซ้ำกัน
			orderid = 'OD' + mid + dt # รวมกันเป็นรหัสID ที่ไม่ซ้ำกันแน่นอน

			for pd in mycart:	
				order = OrderList()
				order.orderid  = orderid # เมื่อได้แล้วไปเก็บลงใน models ของ OrderList
				order.productid = pd.productid # productid มาจาก Mycart runforloop ให้ไปเก็บใน OrderList
				order.productname = pd.productname
				order.price = pd.price
				order.quantity = pd.quantity
				order.total = pd.total
				order.save()

			# EP14 Create OderPinding 
			# พวก user,name,tel,address,shipping,payment,other มาจาก หน้า html เดียวกันไม่ต้อง get ค่าใหม่
			odp = OrderPending()
			odp.orderid = orderid # ต้องเป็น orderid เดียวกัน กับ OrderList เพราะจะได้เป็น ID เดียวกัน
			odp.user  = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()
			###### เมื่อ Save เสร็จให้เคลียข้อมูล
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0 
			updatequan.save()
			return redirect('mycart-page')

	return render(request, 'myapp/checkout1.html')


#EP15 โชว์สถานะของการสั่งซื้อ
def OrderListPage(request):
	
	username = request.user.username
	user = User.objects.get(username=username)
	context =  {}

	# join 2 ตารางรวมกันเพื่อเอาข้อมูลmodels ไปใส่อีก models แต่จะเป็นการชั่วคราว 
	order  = OrderPending.objects.filter(user=user)  # filter จะใช้กับหลายรายการ
	for od in order:
		orderid = od.orderid # ดึงรายการ order ออกมา ของ order ออกมา
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([ c.total for c in odlist])
		od.total = total

	context['allorder'] = order # ส่งข้อความแบบ dic  ['allorder'] คือ ชื่อ key

	return render(request, 'myapp/orderlist.html',context)

def AllOrderListPage(request):
	
	# username = request.user.username
	# user = User.objects.get(username=username)
	# ไม่ใส่เพราะว่าต้องการเห็นทั้งหมด ไม่เจาะจงว่าเป็น User ไหน
	context =  {}

	order  = OrderPending.objects.all()  # filter จะใช้กับหลายรายการ
	for od in order:
		orderid = od.orderid # ดึงรายการ order ออกมา
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([ c.total for c in odlist])
		od.total = total

	context['allorder'] = order # ส่งข้อความแบบ dic  ['allorder'] คือ ชื่อ key

	return render(request, 'myapp/allorderlist.html',context)

# EP 16 Uploadslip
def UploadSlip(request,orderid): # orderid มาจาก OrderList ของ models
	print('ORDER ID:',orderid)

	# EP8  import FileSystemStorage เพื่อทำ Upload ข้อมูลจากเครื่อง
	if request.method == 'POST' and request.FILES['slip']:
		data = request.POST.copy()
		sliptime = data.get('sliptime')
		update = OrderPending.objects.get(orderid=orderid)
		update.sliptime = sliptime

		############# EP8 Save Image ##############
		file_image = request.FILES['slip']
		file_image_name = request.FILES['slip'].name.replace(' ','') # ถ้าชื่อไฟล์มี Spech จะrepalce
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		update.slip = upload_file_url[6:] # [6:] คือการ slide ข้าม media
		update.save()

	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum([ c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid)
	# คำนวนค่าส่งตามประเภท
	
	count = sum([ c.quantity for c in odlist])
	if oddetail.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		# shipcost =  ค่ารวมทั้งหมด (หากเป็นชิ้นแรกค่าส่งจะคิด 50 บาท ชัดถัดไป 10 บาท)
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])

	if oddetail.payment == 'cod': # cod มาจาก html ของ checkout1
		shipcost += 20 # shipcost = shipcost + 20

	context = {'orderid':orderid,
				'total':total,
				'shipcost':shipcost,
				'grandtotal':total+shipcost,
				'oddetail':oddetail,
				'count':count}


	return render(request, 'myapp/uploadslip.html',context)
