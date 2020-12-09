from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "Catégorie"



class FoodMenu(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, null=True)
    category = models.ManyToManyField(category, null=True)
    details = models.TextField(null=True)
    date = models.DateTimeField(null=True, blank=True)
    picture1 = models.ImageField(null=True, blank=True,upload_to='images/')
    picture2 = models.ImageField(null=True, blank=True,upload_to='images/')
    picture3 = models.ImageField(null=True, blank=True,upload_to='images/')
    slug = models.SlugField(blank=True, unique=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return  str(self.name)

    class Meta:
        verbose_name_plural = "Food-Menu"

class Comment(models.Model):
    menu = models.ForeignKey(FoodMenu, null=True, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE,related_name='user')
    comment = models.TextField(blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,  null=True)

    def __str__(self):
        return 'Comment =  {} By {}'.format(self.comment, self.user.username)
        
    class Meta:
        verbose_name_plural = "Comments"
        ordering = ['created_at']


class Contacter_nous(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200,null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return  self.full_name

    class Meta:
        verbose_name_plural = "Contacter_nous"



class Subcribe(models.Model):
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Abonnement par courrier électronique"