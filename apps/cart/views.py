from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from apps.shop.models import ProductModel
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = ProductModel.get_object_or_404(id=product_id)
        cart.add(product)
        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
        }
        return JsonResponse(context)
    except:
        context = {
            {'error': 'invalid request'},
        }
        return JsonResponse(context)
