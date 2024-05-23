from django.contrib import admin
from .models import (
    ProductModel, ProductFeatureModel,
    ProductCategoryModel, ProductImageModel
)


class ProductFeatureInline(admin.StackedInline):
    model = ProductFeatureModel
    extra = 0
    show_change_link = True
    classes = ['collapse']


class ProductImageInline(admin.StackedInline):
    model = ProductImageModel
    extra = 0
    show_change_link = True
    classes = ['collapse']


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ['created']
    search_fields = ['title']


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'inventory', 'price', 'off', 'new_price']
    list_filter = ['created']
    search_fields = ['title']
    raw_id_fields = ['category']
    inlines = [ProductFeatureInline, ProductImageInline]


@admin.register(ProductFeatureModel)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']
    list_filter = ['created']
    search_fields = ['key', 'value']
    raw_id_fields = ['product']


@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_filter = ['created']
    raw_id_fields = ['product']
