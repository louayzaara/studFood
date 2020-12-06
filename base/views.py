from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base.html')

def HomePage(request):
    return render(request, 'home.html')