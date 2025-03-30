from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, View
from django.http import HttpResponse
from .models import *
from .forms import *
from django.http import request
from django.urls import reverse_lazy

def HomePage(request):
    return render(request, 'main_hd/HomePage.html', {'title': 'Home page'})

def SingUp(request):
    return render(request, 'main_hd/SingUp.html', {'title': 'Make an appointment'})


def Reviews(request):
    rm = ReviewsModel.objects.all().order_by('-id')
    
    paginator = Paginator(rm, 15)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    client_ip = get_client_ip(request=request)
    is_unique = ReviewsModel.objects.filter(ip=client_ip).exists()
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            try:
                ReviewsModel.objects.create(**form.cleaned_data)
                return redirect('reviews')
            except:
                return redirect('reviews')

    else:
        form = ReviewsForm()

    return render(request, "main_hd/reviews.html", {'title': 'Reviews', 'Reviews': page_obj, 'ip': client_ip, 'is_unique': is_unique, 'page_obj': page_obj})

def get_client_ip(request):        
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
        print(x_forward_for.split(','))
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def OurServices(request):
    services = Category.objects.all()
    return render(request, 'main_hd/OurServices.html', {'title': 'Services', 'services': services})

class OurServicesDetail(ListView):
    paginate_by = 10
    model = HairdressModel
    template_name = 'main_hd/OurServicesDetail.html'
    extra_context = {'title': 'Services'}
    context_object_name = 'serviceDetailes'

    def get_queryset(self):
        return HairdressModel.objects.filter(cat_id=self.kwargs['category_id']).order_by('-id')