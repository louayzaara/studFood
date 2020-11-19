from django.urls import path, include
from . import views
 
app_name="studfood"

urlpatterns = [
     path('home/', views.homePage, name="home-page")
 ]