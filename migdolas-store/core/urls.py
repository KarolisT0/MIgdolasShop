from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🛒 Product-related views
    path('parduotuve/', views.product_list, name='product_list'),
    path('parduotuve/kategorija/<slug:category_slug>/', views.product_list, name='product_list_by_category'),


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
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # orders
    path('mano-uzsakymai/', views.order_history, name='order_history'),
    path('mano-uzsakymai/<str:order_number>/', views.order_detail, name='order_detail'),


    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
