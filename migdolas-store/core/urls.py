from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🛒 Product-related views
    path('parduotuve/', views.product_list, name='product_list'),

    # 🛒 Cart functionality
    path('cart/', views.cart_detail, name='cart_detail'),  # ✅ Fixed view name
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),

    # 💳 Checkout
    path('checkout/', views.checkout, name='checkout'),

    # 📝 TinyMCE
    path('tinymce/', include('tinymce.urls')),

    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
