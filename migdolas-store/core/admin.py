from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, Order, OrderItem


# -------- ORDER ADMIN --------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at', 'total_price')
    search_fields = ('id', 'name', 'email', 'phone')
    list_filter = ('created_at',)
    list_display_links = ('id', 'name')
    inlines = [OrderItemInline]

    def total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())


# -------- PRODUCT ADMIN --------
class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    inlines = [ProductImageInline, ProductVariantInline]
