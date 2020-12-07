from django.urls import path, include
from . import views
 
app_name="studfood"

urlpatterns = [
     path('home/', views.homePage, name="home-page"),
     path('', views.homePage, name="home-page"),
     path('menu-info/<int:id>/',views.signleMenuPage, name="single-menu"),
     path('contacter-nous/', views.ContactusPage, name="contactus-page"),
 ]