from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
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
    path('order-success/<str:order_number>/', views.order_success, name='order_success'),

    # # 🔒 Authentication
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='product_list'), name='logout'),

    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
