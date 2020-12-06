from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FoodMenu(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, null=True)
    details = models.TextField(null=True)
    date = models.DateTimeField(null=True, blank=True)
    picture1 = models.ImageField(null=True, blank=True,upload_to='images/')
    picture2 = models.ImageField(null=True, blank=True,upload_to='images/')
    slug = models.SlugField(blank=True, unique=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return  str(self.user)

    class Meta:
        verbose_name_plural = "Food-Menu"

