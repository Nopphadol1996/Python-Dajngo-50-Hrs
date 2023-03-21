from django.shortcuts import render
from django.http import HttpResponse
# django คือ แพ็คเกจ หลัก .http คือ แพ็คเกจย่อย  HttpResponse คือฟังก์ชั่นที่ทำให้โชว์ข้อความหน้าเว็บได้

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


