import json
import random
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from apps.accounts.models import User
from apps.cart.cart import Cart
from apps.orders.models import OrderItemModel, OrderModel
from config.settings import CallbackURL, MERCHANT, ZP_API_REQUEST, ZP_API_STARTPAY, ZP_API_VERIFY
from .forms import PhoneVerificationForm, OrderCreateForm


def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('orders:order_create')
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if User.objects.filter(phone=phone).exists():
                messages.error(request, 'this phone is already registered.')
                return redirect('orders:verify_phone')
            else:
                tokens = {'token': ''.join(random.choices('0123456789', k=6))}
                request.session['verification_code'] = tokens['token']
                request.session['phone'] = phone
                print(tokens)
                # send_sms_with_template(phone, tokens, 'verify')
                messages.error(request, 'verification code sent successfully.')
                return redirect('orders:verify_code')
    else:
        form = PhoneVerificationForm()
    return render(request, 'orders/verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if code == verification_code:
                user = User.objects.create_user(phone=phone)
                user.set_password('123456')
                user.save()
                # send sms
                print(user)
                login(request, user)
                del request.session['verification_code']
                del request.session['phone']
                return redirect('orders:order_create')
            else:
                messages.error(request, 'Verification code is incorrect.')
    return render(request, 'orders/verify_code.html')


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.user = request.user
            order.save()
            for item in cart:
                OrderItemModel.objects.create(
                    order=order, product=item['product'],
                    price=item['price'], quantity=item['quantity'],
                    weight=item['weight']
                )
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:request')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})


def send_request(request):
    order = OrderModel.objects.get(id=request.session['order_id'])
    description = ""
    for item in order.order_items.all():
        description += item.product.name + ", "
    data = {
        "MerchantID": MERCHANT,
        "Amount": order.get_final_cost(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(request):
    order = OrderModel.objects.get(id=request.session['order_id'])
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']
            if response_json['Status'] == 100:
                for item in order.items.all():
                    item.product.inventory -= item.quantity
                    item.product.save()
                order.paid = True
                order.save()
                return render(request, 'orders/payment-tracking.html',
                              {"success": True, 'RefID': reference_id, "order_id": order.id})
            else:
                return render(request, 'orders/payment-tracking.html',
                              {"success": False})
        del request.session['order_id']
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def orders_list(request):
    orders = OrderModel.objects.filter(user=request.user)
    return render(request, 'orders/orders-list.html', {'orders': orders})


def order_detail(request, id):
    order = OrderModel.objects.get(user=request.user, id=id)
    return render(request, 'orders/order-detail.html', {'order': order})
