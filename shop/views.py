from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import *
from .models import Catagory, Cart

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
    if not request.user.is_authenticated:
        messages.error(request, "Please login to add items to cart.")
        return redirect('login')

    if request.method == 'POST':
        product = get_object_or_404(Product, id=id, status=0)
        if product.quantity and product.quantity > 0:
            try:
                quantity_to_add = int(request.POST.get('quantity', 1))
                if quantity_to_add < 1:
                    messages.error(request, "Quantity must be at least 1.")
                    return redirect('product_detail', id=id)
            except ValueError:
                messages.error(request, "Invalid quantity.")
                return redirect('product_detail', id=id)

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 0}
            )
            new_quantity = cart_item.quantity + quantity_to_add
            if new_quantity > product.quantity:
                messages.error(request, f"Cannot add {quantity_to_add} more {product.name}. Only {product.quantity - cart_item.quantity} left in stock.")
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, f"{quantity_to_add} {product.name} added to cart!")
        else:
            messages.error(request, f"{product.name} is out of stock.")
        return redirect('product_detail', id=id)
    return redirect('collections')

def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to view your cart.")
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.total_price for item in cart_items)
    cart_items_list = []
    for item in cart_items:
        cart_items_list.append({
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.selling_price,
            'quantity': item.quantity,
            'image': item.product.product_image.url if item.product.product_image else '',
            'total': item.total_price
        })
    return render(request, "shop/cart.html", {"cart_items": cart_items_list, "total": total})

def remove_from_cart(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to remove items from cart.")
        return redirect('login')

    product = get_object_or_404(Product, id=id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, f"{product.name} removed from cart!")
    else:
        messages.error(request, "Item not found in cart.")
    return redirect('cart')

def user_logout(request):
    logout(request)
    return redirect('home')
