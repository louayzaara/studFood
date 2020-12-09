from django.urls import path, include
from . import views
 
app_name="studfood"

urlpatterns = [
     path('home/<int:id>', views.homePage, name="home-page"),
     path('menu-info/<int:id>/',views.signleMenuPage, name="single-menu"),
     path('contacter-nous/', views.ContactusPage, name="contactus-page"),
     path('', views.welcomePage, name="welcome-page"),
     path('search/',views.searchPage, name="search-page"),
     path('search-profile/',views.searchProfilePage, name="search-profile-page"),

 ]