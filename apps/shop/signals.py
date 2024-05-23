from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ProductModel


@receiver(signal=pre_save, sender=ProductModel)
def calculate_total_price(sender, instance: ProductModel, **kwargs):
    instance.new_price = instance.price - instance.off
