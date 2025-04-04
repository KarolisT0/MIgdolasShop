from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .cart import Cart
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart_detail')

@require_POST
def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    product_id_str = str(product_id)

    if product_id_str in cart.cart:
        cart.cart[product_id_str]['quantity'] = quantity
        cart.save()

    return redirect('cart_detail')