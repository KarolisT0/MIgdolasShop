import time
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.crypto import get_random_string
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# -------------------
# category
# -------------------

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    def category_context(request):
        return {
            'categories': Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    }

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# -------------------
# Product
# -------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = HTMLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_price_range(self):
        prices = list(self.variants.values_list('price', flat=True))
        if prices:
            return min(prices), max(prices)
        return self.price, self.price

# -------------------
# Product Images
# -------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"


# -------------------
# Product Variants
# -------------------
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g. "2.5S", "Banketė"
    size = models.CharField(max_length=100)  # e.g. "200x90x75"
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.size} - {self.price} €"


# -------------------
# Order
# -------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Laukiama'),
        ('processing', 'Vykdoma'),
        ('shipped', 'Išsiųsta'),
        ('completed', 'Įvykdyta'),
        ('cancelled', 'Atšaukta'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.order_number} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            for _ in range(5):
                candidate = self.generate_order_number()
                if not Order.objects.filter(order_number=candidate).exists():
                    self.order_number = candidate
                    break
                time.sleep(0.1)
            else:
                self.order_number = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S%f')}"
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            time.sleep(0.1)
            return self.save(*args, **kwargs)

    def generate_order_number(self):
        date_str = timezone.now().strftime("%Y%m%d")
        random_str = get_random_string(length=5, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        return f"ORD{date_str}{random_str}"
    
    @property
    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())


# -------------------
# Order Item
# -------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# -------------------
# Profiles
# -------------------

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username