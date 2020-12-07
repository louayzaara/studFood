from django.contrib import admin
from .models import FoodMenu, Comment, Contacter_nous, category
# Register your models here.

admin.site.register(FoodMenu)
admin.site.register(Comment)
admin.site.register(Contacter_nous)
admin.site.register(category)

