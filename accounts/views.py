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
                messages.error(request,"username should be more than 8 digits!")
                return redirect("accounts:register-page")

            userCheck = User.objects.filter(username=username)
            if userCheck:
                messages.error(request,"username is already taken, try another!")
                return redirect("accounts:register-page")

            checkMail = User.objects.filter(email=email)
            if checkMail:
                messages.error(request,"Email is already taken by an other user!")
                return redirect("accounts:register-page")

            if password1 != password2:
                messages.error(request,"Password doesn't match please try again!")
                return redirect("accounts:register-page")

            if form.is_valid():
                email = request.POST['email']
                user = form.save()
                user.is_active = False
                user.email = email
                user.save()
                email = request.POST['email']

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('accounts:activate', kwargs={
                    'uidb64':uidb64,
                    'token':generate_token.make_token(user)})
                activate_url = 'https://'+domain+link
                email_body = 'Hi' +' ' +user.username + '\nPlease use this link to verify your account  \n' +activate_url + '\n\nThanks for using our site!' +'\nThe '+domain  +' team'
                email_subject = 'accounts activation'
                to_email = email
                email = EmailMessage(
                    email_subject, email_body, to=[to_email]
                )
                email.send()
                username = request.POST.get('username')
                messages.success(request, 'Account was created for ' + username + '  ' + 'please check your email address to verify your account !')
                return redirect('accounts:login-page')

            else:
                messages.error(request,"Something went wrong, Please try again!")
                return redirect("accounts:register-page")


    context = {

        'form':form,

    }
    return render(request, 'register.html',context)

# def RegisterPage(request):
#     return render(request, 'register.html')

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

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login to  your account.')
    else:
        return HttpResponse('Activation link is invalid!')

