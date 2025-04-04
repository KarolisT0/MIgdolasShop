import string
import random
import time
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.crypto import get_random_string
from tinymce.models import HTMLField



class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = HTMLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g. "2.5S", "Banketė"
    size = models.CharField(max_length=100)  # e.g. "200x90x75"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.size} - {self.price} €"

class Order(models.Model):
    order_number = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_number} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            for attempt in range(5):  # Try up to 5 times
                order_number = self.generate_order_number()
                if not Order.objects.filter(order_number=order_number).exists():
                    self.order_number = order_number
                    break
                time.sleep(0.1)
            else:
                # Fallback: full timestamp-based number
                self.order_number = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S%f')}"

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            time.sleep(0.1)
            return self.save(*args, **kwargs)

    def generate_order_number(self):
        date_str = timezone.now().strftime("%Y%m%d")
        while True:
            random_str = get_random_string(length=5, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            order_number = f"ORD{date_str}{random_str}"
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
