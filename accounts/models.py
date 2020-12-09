from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.utils.text import slugify

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True,blank=True)
    email = models.EmailField(max_length=30,null=True,blank=True)
    phone_number = models.CharField(max_length=20, null=True,blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_picture = models.ImageField(default="default_logo.png",null=True, blank=True,upload_to='images/')
    gender = models.CharField(max_length=25, null=True,blank=True)
    university = models.CharField(max_length=25, null=True,blank=True)
    slug = models.SlugField(blank=True, unique=True,null=True)
    is_verified = models.BooleanField(default=True,blank=True)
    is_restaurant = models.BooleanField(default=False,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return  str(self.user)

    class Meta:
        verbose_name_plural = "Profile"

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'],
        slug = slugify(str(kwargs['instance']) + '-' +'1')
        )
post_save.connect(create_profile, sender=User)
