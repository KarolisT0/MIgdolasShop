from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, Order, OrderItem, Category, UserProfile
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html


# -------- ORDER ADMIN --------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at', 'total_price', 'status', 'colored_status')
    search_fields = ('id', 'name', 'email', 'phone')
    list_filter = ('created_at', 'status')
    list_editable = ('status',)
    list_display_links = ('id', 'name')
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        if change:
            original = Order.objects.get(pk=obj.pk)
            if original.status != obj.status:
                # 🔔 Status has changed — send email
                send_mail(
                    subject=f"Užsakymo būsena atnaujinta: {obj.order_number}",
                    message=f"Jūsų užsakymo būsena pakeista į: {obj.get_status_display()}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email, settings.ADMIN_EMAIL],
                )
        super().save_model(request, obj, form, change)

    def colored_status(self, obj):
        color_map = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'teal',
            'completed': 'green',
            'cancelled': 'red',
        }
        color = color_map.get(obj.status, 'black')
        return format_html('<strong style="color: {}">{}</strong>', color, obj.get_status_display())

    colored_status.short_description = 'Statusas'


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
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
