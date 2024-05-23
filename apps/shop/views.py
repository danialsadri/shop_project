from django.shortcuts import render
from .models import ProductModel, ProductCategoryModel


def product_list(request, category_slug=None):
    category = None
    categories = ProductCategoryModel.objects.all()
    products = ProductModel.objects.all()
    if category_slug:
        category = ProductCategoryModel.get_object_or_404(slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_id, product_slug):
    product = ProductModel.get_object_or_404(id=product_id, slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'shop/product_detail.html', context)
