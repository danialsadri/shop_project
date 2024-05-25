from django.contrib import admin
from .actions import export_to_excel
from .models import OrderModel, OrderItemModel


class OrderItemInline(admin.StackedInline):
    model = OrderItemModel
    extra = 0
    show_change_link = True
    classes = ['collapse']
    raw_id_fields = ['order', 'product']


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'paid']
    list_filter = ['created', 'paid']
    search_fields = ['name', 'phone']
    raw_id_fields = ['user']
    inlines = [OrderItemInline]
    actions = [export_to_excel]


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'weight']
    list_filter = ['created']
    raw_id_fields = ['order', 'product']
