from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('list/', views.product_list, name='product_list'),
    path('list/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('detail/<int:product_id>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
