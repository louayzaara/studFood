from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodMenu, Comment, category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import FoodMenuFilter
from .forms import CommentForm,ContactUsForm
from django.contrib import messages
from django.conf import settings
import json
import urllib
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from accounts.models import Profile
from django.contrib.auth.models import User
from .filters import ProfileFilter
# Create your views here.
def searchPage(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post =  Profile.objects.all().filter(first_name=search) or Profile.objects.all().filter(last_name=search) 
        context = {
            'post':post
            }
        return render(request,'search_page.html',context)

def searchProfilePage(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post =  FoodMenu.objects.all().filter(name=search) 
        context = {
            'post':post
            }
        return render(request,'search_profile_page.html',context)



def welcomePage(request):

    if request.user.username:
        user = User.objects.get(username=request.user.username)
        if not user.profile.first_name or not user.profile.last_name or not user.profile.university or not user.profile.phone_number:
            messages.info(request, 'afin de continuer à utiliser notre plateforme, veuillez mettre à jour vos informations de profil!')
            return redirect('accounts:edit-profile-page')

    rest_list = Profile.objects.filter(is_restaurant=True)

    Filter = ProfileFilter(request.GET, queryset=rest_list)
    rest_list = Filter.qs

    page = request.GET.get('page')
    paginator = Paginator(rest_list, 6)
    try:
        rest_list = paginator.page(page)
    except PageNotAnInteger:
        rest_list = paginator.page(1)
    except EmptyPage:
        rest_list = paginator.page(paginator.page_range)
    context = {
        'rest_list':rest_list,
    }
    return render(request, 'welcome.html',context)


def homePage(request,id):
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        if not user.profile.first_name or not user.profile.last_name or not user.profile.university or not user.profile.phone_number:
            messages.info(request, 'afin de continuer à utiliser notre plateforme, veuillez mettre à jour vos informations de profil!')
            return redirect('accounts:edit-profile-page')
            
    if User.objects.filter(id=id).exists():
        rest_menu_list = FoodMenu.objects.filter(user=id)
    else:
        return redirect('studfood:welcome-page')
    menu_list = FoodMenu.objects.filter(user=id)
    category_list = category.objects.all()
    Filter = FoodMenuFilter(request.GET, queryset=menu_list)
    menu_list = Filter.qs

    page = request.GET.get('page')
    paginator = Paginator(menu_list, 3)
    try:
        menu_list = paginator.page(page)
    except PageNotAnInteger:
        menu_list = paginator.page(1)
    except EmptyPage:
        menu_list = paginator.page(paginator.page_range)
    context = {
        'menu_list':menu_list,
        'Filter':Filter,
        'category_list':category_list
    }
    return render(request, 'acceuil.html',context)


def signleMenuPage(request, id):
    if FoodMenu.objects.filter(id=id).exists():
        singleMenu = FoodMenu.objects.filter(id=id)
    else:
        return redirect('studfood:home-page')
    
    menu = get_object_or_404(FoodMenu, id=id)
    comments_list = menu.comments.all()
    comment_number = comments_list.count()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Merci pour  votre commentaire!')
        else:
            messages.info(request, 'erreur!')

    else:
        form = CommentForm(request.POST)

    context = {
        'singleMenu':singleMenu,
        'form':form,
        'comment_number':comment_number,
        'comments_list':comments_list
    }
    return render(request, 'single_menu.html',context)


def ContactusPage(request):
    form = ContactUsForm(request.POST)
    recaptcha = True
    failed_recaptcha = False
    secret = getattr(settings, 'GOOGLE_RECAPTCHA_SECRET_KEY', None)
    public_key = getattr(settings, 'GOOGLE_RECAPTCHA_PUBLIC_KEY', None)

    if request.method == 'POST':
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': secret,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                form.save()
                form = ContactUsForm(request.POST)
                messages.info(request, 'votre message a été envoyé, vous recevrez une réponse dans les plus brefs délais, merci de nous contacter!')
        else:
            form = ContactUsForm(request.POST)
            recaptcha = True
            failed_recaptcha = True

            args = {
                    'form':form,
                    'recaptcha':recaptcha,
                    'public_key':public_key,
                    'failed_recaptcha':failed_recaptcha,

                    }
            return render(request, 'contact_us.html',args)
    args = {
            'form':form,
            'recaptcha':recaptcha,
            'public_key':public_key,
            'failed_recaptcha':failed_recaptcha,

            }
    return render(request, 'contact_us.html',args)
