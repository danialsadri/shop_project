from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('detail/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
