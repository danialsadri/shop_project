from apps.shop.models import ProductModel
from config.settings import CART_SESSION_ID


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()
        for product in products:
            cart_dict[str(product.id)]['product'] = product
        for item in cart_dict.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def get_post_price(self):
        weight = sum(item['weight'] * item['quantity'] for item in self.cart.values())
        if weight < 1000:
            return 20000
        elif 1000 <= weight < 2000:
            return 30000
        else:
            return 50000

    def save(self):
        self.session.modified = True
