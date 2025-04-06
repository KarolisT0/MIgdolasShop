from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.conf import settings

from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm
from django.core.mail import send_mail


# ----------------------
# 🏠 Home + Product Views
# ----------------------
def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'home.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    similar_products = Product.objects.exclude(id=product.id)[:4]

    return render(request, 'product_detail.html', {
        'product': product,
        'similar_products': similar_products,
    })


# ----------------------
# 🛒 Cart Views
# ----------------------
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    variant_id = request.POST.get('variant_id')
    if product.variants.exists() and variant_id:
        variant = product.variants.get(id=variant_id)
        item_name = f"{product.name} ({variant.name} - {variant.size})"
        price = variant.price
    else:
        item_name = product.name
        price = product.price

    cart.add(product=product, name=item_name, price=price)
    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
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


# ----------------------
# 💳 Checkout
# ----------------------
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product_obj'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            send_mail(
                subject=f"Užsakymas patvirtintas – {order.order_number}",
                message=(
                    f"Ačiū, {order.name}!\n\n"
                    f"Jūsų užsakymas #{order.order_number} buvo gautas.\n"
                    f"Prekių kiekis: {order.items.count()}\n"
                    f"Mes susisieksime su Jumis greitai.\n\n"
                    f"Migdolas"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email, settings.ADMIN_EMAIL],
                fail_silently=False
            )


            cart.clear()
            return redirect('order_success', order_number=order.order_number)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'cart': cart})

def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    total = sum(item.price * item.quantity for item in order.items.all())

    return render(request, 'order_success.html', {
        'order': order,
        'total': total,
    })