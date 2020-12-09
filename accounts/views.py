from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib.auth.models import User
from .utils import TokenGenerator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_token
from django.urls import reverse
from django.http import HttpResponse
from .forms import EditProfileForm
# Create your views here.

def ProfilePage(request):
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        if not user.profile.first_name or not user.profile.last_name or not user.profile.university or not user.profile.phone_number:
            messages.info(request, 'afin de continuer à utiliser notre plateforme, veuillez mettre à jour vos informations de profil!')
            return redirect('accounts:edit-profile-page')
    return render(request, 'profile.html')

def EditProfilePage(request):
    user=request.user.profile
    form = EditProfileForm(instance=user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated!')
            return redirect('accounts:profile-page')
    context = {
        'form':form
    }
    return render(request, 'edit_profile.html',context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('studfood:home-page')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if len(username) < 8:
                messages.error(request,"le nom d'utilisateur doit comporter plus de 8 chiffres!")
                return redirect("accounts:register-page")

            userCheck = User.objects.filter(username=username)
            if userCheck:
                messages.error(request,"le nom d'utilisateur est déjà pris, essayez-en un autre!")
                return redirect("accounts:register-page")

            checkMail = User.objects.filter(email=email)
            if checkMail:
                messages.error(request,"E-mail est déjà pris par un autre utilisateur!")
                return redirect("accounts:register-page")

            if password1 != password2:
                messages.error(request,"Mot de passe ne correspond pas, veuillez réessayer!")
                return redirect("accounts:register-page")

            if form.is_valid():
                email = request.POST['email']
                user = form.save()
                user.is_active = True
                user.email = email
                user.save()
                username = request.POST.get('username')
                messages.success(request, 'Le compte a été créé pour  ' + username + '  ' )
                return redirect('accounts:login-page')

            else:
                messages.error(request,"Une erreur s'est produite. Veuillez réessayer!")
                return redirect("accounts:register-page")

    context = {
        'form':form,
    }
    return render(request, 'register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('studfood:welcome-page')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user :
                if  user.is_active:
                    login(request, user)
                    return redirect('studfood:welcome-page')
                else:
                    messages.info(request, "Une erreur s'est produite. Veuillez réessayer!")
                    return redirect('accounts:login-page')
            else:
                messages.error(request, "Le nom d'utilisateur ou le mot de passe sont incorrects")
                return redirect('accounts:login-page')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login-page')
