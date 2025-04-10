from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView, profile_view, CustomLoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🛒 Product-related views
    path('parduotuve/', views.product_list, name='product_list'),
    path('parduotuve/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('parduotuve/<slug:category_slug>/<slug:subcategory_slug>/', views.product_list, name='product_list_by_subcategory'),



    # 🛒 Cart functionality
    path('vezimelis/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('ajax/search/', views.ajax_product_search, name='ajax_product_search'),

    # 💳 Checkout
    path('atsiskaitymas/', views.checkout, name='checkout'),

    # 📝 TinyMCE
    path('tinymce/', include('tinymce.urls')),
    path('uzsakymas/<str:order_number>/', views.order_success, name='order_success'),

    # # 🔒 Authentication
    path('registracija/', views.register, name='register'),
    path('prisijungimas/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('atsijungimas/', CustomLogoutView.as_view(), name='logout'),
    path('slaptazodio-atkurimas/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # # Orders
    path('mano-uzsakymai/', views.order_history, name='order_history'),
    path('mano-uzsakymai/<str:order_number>/', views.order_detail, name='order_detail'),

    # # Profile
    path('profilis/', profile_view, name='profile'),

    #  # Other pages
    path('apie-mus/', views.about, name='about'),
    path('kontaktai/', views.contacts_view, name='contacts'),
    path('baldu-prieziura/', views.cleaning_view, name='cleaning'),

    


    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
