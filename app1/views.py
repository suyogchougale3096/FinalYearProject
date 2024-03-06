from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib import messages

def landingpage(request):
    data = {
        'title' : 'Home Page',
        'image1' : 'Our product provides expert recommendations for your investment portfolio, saving you time and effort in researching and analyzing investment options.',
        'image2' : 'With our product, you can easily build a diversified portfolio that aligns with your financial goals. We take into account your risk tolerance, investment horizon, and financial objectives.',
        'image3' : 'Our expert recommendations help you make informed investment decisions to achieve your financial goals. Whether youre saving for retirement, buying a house, or funding your child education, weve got you covered.'
    }
    return render(request,"MainPage.html",data)

def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')

        user = authenticate(request,username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return HttpResponse("valid credentials")
        else:
            return HttpResponse("Invalid credentials")
    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email1 = request.POST.get('email1')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('cpassword1')

        user = authenticate(request,username=uname, password=pass1)
        if(user is None):
            if(len(pass1) <= 8 or pass1 != pass2 or len(uname) <= 8):
                return HttpResponse("1. Enter the valid username. Length must be greater than 8.\n2. The password length should be greater than 8. \n3. The entered password and confirmed password should be match.")
            else:
                my_user = User.objects.create_user(uname,email1,pass1)
                return redirect('login')
        else:
            return HttpResponse('usename is already present try different.')
    return render(request,"signup.html")