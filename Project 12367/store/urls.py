from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/update_status/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
    path('thank_you/<int:order_id>/', views.thank_you, name='thank_you'),
]
