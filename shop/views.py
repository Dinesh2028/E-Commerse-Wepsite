from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import *
from .models import Catagory

# Create your views here.
def home(request):
    trending_products = Product.objects.filter(status=0, trending=True).order_by('-created_at')
    return render(request,"shop/index.html", {"trending_products": trending_products})

def register(request):
    return render(request,"shop/register.html")

def collections(request):
    categories = Catagory.objects.filter(status=0).prefetch_related('product_set')
    return render(request,"shop/collections.html",{"categories": categories})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id, status=0)
    return render(request, "shop/product_detail.html", {"product": product})

def add_to_cart(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id, status=0)
        if product.quantity and product.quantity > 0:
            cart = request.session.get('cart', {})
            product_id = str(id)
            if product_id in cart:
                if cart[product_id]['quantity'] < product.quantity:
                    cart[product_id]['quantity'] += 1
                    messages.success(request, f"{product.name} added to cart!")
                else:
                    messages.error(request, f"Cannot add more {product.name}. Stock limit reached.")
            else:
                cart[product_id] = {
                    'name': product.name,
                    'price': product.selling_price,
                    'quantity': 1,
                    'image': product.product_image.url if product.product_image else ''
                }
                messages.success(request, f"{product.name} added to cart!")
            request.session['cart'] = cart
        else:
            messages.error(request, f"{product.name} is out of stock.")
        return redirect('product_detail', id=id)
    return redirect('collections')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        item_total = item['price'] * item['quantity']
        total += item_total
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'total': item_total
        })
    return render(request, "shop/cart.html", {"cart_items": cart_items, "total": total})

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)
    if product_id in cart:
        product_name = cart[product_id]['name']
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, f"{product_name} removed from cart!")
    else:
        messages.error(request, "Item not found in cart.")
    return redirect('cart')

def user_logout(request):
    logout(request)
    return redirect('home')
