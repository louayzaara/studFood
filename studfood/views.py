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
# Create your views here.
def homePage(request):
    menu_list = FoodMenu.objects.all()
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
    admin_email = getattr(settings, 'EMAIL_HOST_USER', None)
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
                email = request.POST['email']
                full_name = request.POST['full_name']
                subject = request.POST['subject']
                domain = get_current_site(request).domain
                email_body = 'bonjour' + ' '  +full_name  +'\n' +'\nNous avons reçu votre demande concernant' +' ' +subject + ' '+ 'et nous vous répondrons dans les plus brefs délais'+'\nMerci d utiliser notre site!' +'\nde la part de '+domain
                email_subject = 'Contact-us'
                to_email = email
                email = EmailMessage(
                    email_subject, email_body, to=[to_email]
                )
                email.send()
                form.save()
                form = ContactUsForm(request.POST)
                messages.info(request, 'Votre message a été envoyé, vous recevrez une réponse dans les plus brefs délais, merci de nous contacter!')
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
