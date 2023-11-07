from django.shortcuts import render,redirect,HttpResponse
from .models import Registration,Query
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.db.models import Q
from project.settings import RAZOPAY_API_KEY, RAZOPAY_API_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@login_required(login_url='login')
@csrf_exempt
def home(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key,val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        user = Registration.objects.filter(order_id=order_id).first()
        user.paid = True
        user.save()
        val = int(user.amount)/100
        dict = {
        'data':user,
        'val':val
        }
        msg_html = render_to_string('email.html',dict)

        msg_plain = "YOU HAVE COMPLETED YOUR ADMISSION PROCESS"

        send_mail("CONGRATULATIONS" ,msg_plain , settings.EMAIL_HOST_USER , [user.email] , html_message = msg_html)


    return render(request,'index.html')

@csrf_exempt
def about(request):
    context = {}
    if request.method == "POST":
        sname = request.POST.get("sname")
        if sname=='':
           return render(request,'nabout.html')
        else:
        
        
           adata = Registration.objects.filter(name__startswith=sname)

           context={"adata":adata}
           return render(request,'about.html',context)
    return render(request,'nabout.html')

def trainer(request):
    return render(request,'trainer.html')

def classes(request):
    return render(request,'classes.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        en=Query(name=name,email=email,message=message)
        en.save()
    return render(request,'contact.html')

def signupPage(request):
    if request.method == 'POST':
       uname=request.POST.get('username')
       email=request.POST.get('email')
       pass1=request.POST.get('pass1')
       pass2=request.POST.get('pass2')

       if pass1!=pass2:
           return HttpResponse("Pass1 is not matched pass2 ")
       else:
           my_user=User.objects.create_user(uname,email,pass1)    
           return redirect('login')
    
    return render(request,'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('pass1')
        user=authenticate(request,username=uname,password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("username or password wrong")
        
    return render(request,'login.html')



client = razorpay.Client(auth=(RAZOPAY_API_KEY, RAZOPAY_API_SECRET_KEY))
def payment(request):
    if request.method == 'POST':
       name=request.POST.get('username')
       email=request.POST.get('email')
       age=request.POST.get('age')
       phone=request.POST.get('phone')   
       amount = 50000
       client = razorpay.Client(auth=("rzp_test_npyA3ZVuOJNZ4S" , "ffkGSCrGYqUtHLLxLpaXujy0"))

       payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})   
       payment_order_id=payment['id']
       
       en = Registration(
            name=name,
            email=email,
            age=age,
            phone=phone,
            amount=amount,
            order_id=payment_order_id,
       )
       en.save()
        
       return render(request,'payment.html',{'payment' : payment})
       
    return render(request,'payment.html')



    