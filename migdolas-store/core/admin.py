from django.contrib import admin
from django import forms
from .models import Product, ProductImage, ProductVariant, Order, OrderItem
from .forms import MultiImageForm  # ✅ Import the helper form


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at', 'total_price')
    search_fields = ('id', 'name', 'email', 'phone')
    list_display_links = ('id', 'name')
    inlines = [OrderItemInline]

    def total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    form = MultiImageForm
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        class WrappedFormSet(formset):
            def save_new(self, form, commit=True):
                images = request.FILES.getlist('images')
                instances = []
                for image in images:
                    instances.append(ProductImage.objects.create(product=obj, image=image))
                return instances

        return WrappedFormSet


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVariantInline]


admin.site.register(Product, ProductAdmin)
