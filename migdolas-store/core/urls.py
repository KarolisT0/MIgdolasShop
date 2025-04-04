from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parduotuve/', views.product_list, name='product_list'),
    path('produktas/<slug:slug>/', views.product_detail, name='product_detail')
]