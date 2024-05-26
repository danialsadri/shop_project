import random
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.accounts.models import User
from apps.cart.cart import Cart
from apps.orders.models import OrderItemModel
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
