from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator

from .models import Product, Order, OrderItem, Category, UserProfile
from .cart import Cart
from .forms import CheckoutForm, CustomUserCreationForm, ProfileForm, CustomLoginForm


# ----------------------
# 🏠 Home + Product Views
# ----------------------
def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    similar_products = Product.objects.exclude(id=product.id)[:4]

    return render(request, 'product_detail.html', {
        'product': product,
        'similar_products': similar_products,
    })

def product_list(request, category_slug=None, subcategory_slug=None):
    category = None
    subcategory = None
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    products = Product.objects.all()

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, parent__isnull=True)
        products = products.filter(category__in=[category] + list(category.subcategories.all()))

    # Filter by subcategory
    if category_slug and subcategory_slug:
        subcategory = get_object_or_404(Category, slug=subcategory_slug, parent=category)
        products = products.filter(category=subcategory)

    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    q = request.GET.get('q')

    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            filtered_products = []
            for product in products:
                price_min, price_max = get_price_range(product)
                if price_max >= min_price and price_min <= max_price:
                    filtered_products.append(product)
            products = filtered_products
        except ValueError:
            pass  # Invalid price input

    if q:
        products = [p for p in products if q.lower() in p.name.lower()]

    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'subcategory': subcategory,
        'categories': categories,
        'products': products,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'q': q or '',
        'page_obj': page_obj,
    }

    return render(request, 'product_list.html', context)

def get_price_range(self):
    prices = list(self.variants.values_list('price', flat=True))
    if prices:
        return min(prices), max(prices)
    return self.price, self.price
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
                user=request.user if request.user.is_authenticated else None,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
            )

            for item in cart:
                product = Product.objects.get(slug=item['slug'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
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
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                initial_data = {
                    'name': request.user.get_full_name(),
                    'email': request.user.email,
                    'address': profile.address,
                    'phone': profile.phone,
                }
                form = CheckoutForm(initial=initial_data)
            except:
                form = CheckoutForm()
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

# ----------------------
# 📝 Order views

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

# ----------------------
# 🔒 Authentication Views

def register(request):
    if request.user.is_authenticated:
        return redirect('product_list')  # or another home page
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registracija sėkminga!")
            return redirect('product_list')
    return render(request, 'registration/register.html', {'form': form})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Atsijungėte sėkmingai.")
        return redirect('login')  # or 'product_list' if preferred
    
class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'
    
# ----------------------
# Profile Views
# ----------------------

@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            profile.save()
            messages.success(request, 'Profilis atnaujintas sėkmingai.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

    return render(request, 'registration/profile.html', {'form': form})
# ----------------------
# Search functionality
# ----------------------


def ajax_product_search(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_slug = request.GET.get('category')

    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(name__icontains=query)

    # Filter using annotated price range (from variants or base price)
    filtered_products = []
    for product in products:
        min_variant_price, max_variant_price = product.get_price_range()

        # Convert input prices to float safely
        try:
            min_price_val = float(min_price) if min_price else None
            max_price_val = float(max_price) if max_price else None
        except ValueError:
            min_price_val = max_price_val = None

        # Check if product fits in range
        if (min_price_val is None or max_variant_price >= min_price_val) and \
           (max_price_val is None or min_variant_price <= max_price_val):
            filtered_products.append(product)

    html = render_to_string('partials/_product_cards.html', {'products': filtered_products})
    return JsonResponse({'html': html})

# ----------------------
# other views
# ----------------------

from django.shortcuts import render

def about(request):
    return render(request, 'about.html')

def contacts_view(request):
    return render(request, 'contacts.html')