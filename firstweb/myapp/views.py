from django.shortcuts import render
from django.http import HttpResponse
# django คือ แพ็คเกจ หลัก .http คือ แพ็คเกจย่อย  HttpResponse คือฟังก์ชั่นที่ทำให้โชว์ข้อความหน้าเว็บได้
from .models import Allproduct # EP5
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
    if request.method == 'POST': # ถ้ามีการส่งค่าจาก HTML
        data = request.POST.copy() # Copy ทั้งหมด ไว้ที่ data
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageurl = data.get('imageurl')
        
         # สร้างตัวแปร new  = Allproduct()  Allproduct คือ database เพื่อที่จะบันทึกข้อมูลใหม่ลงไป
        new.name= name
        new = Allproduct()
        new.price = price
        new.detail = detail
        new.imageurl = imageurl
        new.save()

    return render(request,'myapp/addproduct.html')



