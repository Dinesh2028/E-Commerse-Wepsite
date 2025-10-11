from django.shortcuts import render

# Create your views here.
def home(reqest):
    return render(reqest,"shop/index.html")

def register(reqest):
    return render(reqest,"shop/register.html")