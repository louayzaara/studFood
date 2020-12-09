import django_filters
from django_filters import DateFilter, CharFilter
from .models import FoodMenu
from django.contrib.auth.models import User
from accounts.models import Profile
class FoodMenuFilter(django_filters.FilterSet):

    class Meta:
        model = FoodMenu
        fields = ['name','date']

class ProfileFilter(django_filters.FilterSet):

    class Meta:
        model = Profile
        fields = ['user','first_name','last_name']
        exclude = ['profile_picture','is_restaurant','date_created','is_verified','slug']