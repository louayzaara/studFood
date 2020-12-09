
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Comment, Contacter_nous, Subcribe


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['created_at']

class ContactUsForm(ModelForm):
    class Meta:
        model = Contacter_nous
        fields = '__all__'


class subscriptionForm(ModelForm):
    class Meta:
        model = Subcribe
        fields = '__all__'
