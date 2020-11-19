from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def RegisterPage(request):
    return render(request, 'register.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('studfood:home-page')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user :
                if  user.is_active:
                    login(request, user)
                    return redirect('studfood:home-page')
                else:
                    messages.info(request, 'in order to login , you need to verify your account , please check your email , we already sent you an Activation link!')
                    return redirect('accounts:login-page')
            else:
                messages.error(request, 'Username or Password are incorrect')
                return redirect('accounts:login-page')



    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login-page')