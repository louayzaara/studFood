from django.shortcuts import render
from .models import FoodMenu
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import FoodMenuFilter
# Create your views here.
def homePage(request):
    menu_list = FoodMenu.objects.all()

    Filter = FoodMenuFilter(request.GET, queryset=menu_list)
    menu_list = Filter.qs

    page = request.GET.get('page')
    paginator = Paginator(menu_list, 3)
    try:
        menu_list = paginator.page(page)
    except PageNotAnInteger:
        menu_list = paginator.page(1)
    except EmptyPage:
        menu_list = paginator.page(paginator.page_range)
    context = {
        'menu_list':menu_list,
        'Filter':Filter,
    }
    return render(request, 'acceuil.html',context)