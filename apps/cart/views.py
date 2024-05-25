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


@require_POST
def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    try:
        product = ProductModel.get_object_or_404(id=item_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(product)
        elif action == 'decrease':
            cart.decrease(product)
        else:
            pass
        context = {
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'quantity': cart.cart[item_id]['quantity'],
            'total': cart.cart[item_id]['price'] * cart.cart[item_id]['quantity'],
            'post_price': cart.get_post_price(),
            'final_price': cart.get_final_price(),
        }
        return JsonResponse(context)
    except:
        context = {
            'success': False,
            'error': 'item not found',
        }
        return JsonResponse(context)


@require_POST
def remove_item(request):
    item_id = request.POST.get('item_id')
    try:
        product = ProductModel.get_object_or_404(id=item_id)
        cart = Cart(request)
        cart.remove(product)
        context = {
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'post_price': cart.get_post_price(),
            'final_price': cart.get_final_price(),
        }
        return JsonResponse(context)
    except:
        context = {
            'success': False,
            'error': 'item not found',
        }
        return JsonResponse(context)
