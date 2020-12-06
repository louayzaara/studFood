import django_filters
from django_filters import DateFilter, CharFilter
from .models import FoodMenu
from django.contrib.auth.models import User

class FoodMenuFilter(django_filters.FilterSet):

    class Meta:
        model = FoodMenu
        fields = ['name','date']
