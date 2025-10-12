from django.shortcuts import render
from .models import *
from .models import Catagory

# Create your views here.
def home(request):
    return render(request,"shop/index.html")

def register(request):
    return render(request,"shop/register.html")

def collections(request):
    categories = Catagory.objects.filter(status=0).prefetch_related('product_set')
    return render(request,"shop/collections.html",{"categories": categories})
