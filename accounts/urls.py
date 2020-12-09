from django.urls import path, include
from . import views
 
app_name="accounts"

urlpatterns = [
     path('login/', views.loginPage, name="login-page"),
     path('register/', views.registerPage, name="register-page"),
     path('logout/', views.logoutUser, name="logout"),
     path('oauth/', include('social_django.urls', namespace='social')),
     path('profile/', views.ProfilePage, name='profile-page'),
     path('edit-profile/', views.EditProfilePage, name='edit-profile-page'),
 ]