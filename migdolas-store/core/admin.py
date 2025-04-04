from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at', 'total_price')  # Fields visible in the list
    search_fields = ('id', 'name', 'email', 'phone')  # Fields to search in the admin interface
    list_display_links = ('id', 'name')  # Make "id" and "name" clickable
    inlines = [OrderItemInline]
    def total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    prepopulated_fields = {"slug": ("name",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline]