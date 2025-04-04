from django.contrib import admin
from .models import Product,Order, OrderItem

admin.site.register(Product)

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)