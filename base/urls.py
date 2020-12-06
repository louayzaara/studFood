from django.urls import path, include
from . import views
 
app_name="base"

urlpatterns = [
     path('', views.base, name="base-page"),
     path('home/', views.HomePage, name="home-page")
 ]