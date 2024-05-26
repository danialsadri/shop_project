from django.db import models
from apps.shop.models import ProductModel
from apps.utils.models import BaseModel


class OrderModel(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='order_models', blank=True, null=True, verbose_name='کاربر')
    first_name = models.CharField(max_length=300, verbose_name='نام')
    last_name = models.CharField(max_length=300, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    address = models.CharField(max_length=300, verbose_name='آدرس')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    province = models.CharField(max_length=300, verbose_name='استان')
    city = models.CharField(max_length=300, verbose_name='شهر')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده|نشده')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return self.first_name

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.order_items.all())
        if weight < 1000:
            return 0
        elif 1000 <= weight < 2000:
            return 20000
        elif 2000 <= weight < 4000:
            return 40000
        else:
            return 50000

    def get_final_cost(self):
        return self.get_total_cost() + self.get_post_cost()


class OrderItemModel(BaseModel):
    order = models.ForeignKey(to=OrderModel, on_delete=models.CASCADE, related_name='order_items', verbose_name='سفارش')
    product = models.ForeignKey(to=ProductModel, on_delete=models.CASCADE, related_name='order_items', verbose_name='محصول')
    price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت')
    quantity = models.PositiveBigIntegerField(default=1, verbose_name='تعداد')
    weight = models.PositiveBigIntegerField(default=0, verbose_name='وزن')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم سفارشات'

    def __str__(self):
        return self.order.first_name

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity
