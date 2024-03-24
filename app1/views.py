from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "home.html", {'username': request.user.username})

@login_required
def goal(request):
    return render(request, "goal.html", {'username': request.user.username})

@login_required
def imp(request):
    return render(request, "imp.html", {'username': request.user.username})

def warning(request):
    return render(request,"warning.html")

def usernamewarning(request):
    data = {
        'message' : 'Username is alredy taken please try different.'
    }
    return render(request,"usernamewarning.html",data)

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

        try:
            user = authenticate(request, username=uname, password=pass1)
            if user is not None:
                login(request, user)
                return render(request, "home.html", {'username': uname})
            else:
                return HttpResponse("Invalid credentials")
        except IntegrityError as e:
            return HttpResponse(f"IntegrityError occurred: {str(e)}")
    return render(request,"login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email1 = request.POST.get('email1')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('cpassword1')

        try:
            if len(pass1) <= 8 or pass1 != pass2 or len(uname) <= 8:
                raise ValueError('Invalid input')

            user = User.objects.create_user(uname, email1, pass1)
            return redirect('login')

        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e) and 'username' in str(e):
                return redirect("usernamewarning")
                # return HttpResponse('Username already exists. Please choose a different username.')
            else:
                return HttpResponse('An error occurred during sign up.')

        except ValueError as e:
            return redirect('warning')

    return render(request, "signup.html")