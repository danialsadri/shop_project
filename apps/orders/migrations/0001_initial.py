# Generated by Django 5.0.6 on 2024-05-25 16:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='آیدی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('first_name', models.CharField(max_length=300, verbose_name='نام')),
                ('last_name', models.CharField(max_length=300, verbose_name='نام')),
                ('phone', models.CharField(max_length=11, verbose_name='شماره تلفن')),
                ('address', models.CharField(max_length=300, verbose_name='آدرس')),
                ('postal_code', models.CharField(max_length=10, verbose_name='کد پستی')),
                ('province', models.CharField(max_length=300, verbose_name='استان')),
                ('city', models.CharField(max_length=300, verbose_name='شهر')),
                ('paid', models.BooleanField(default=False, verbose_name='پرداخت شده|نشده')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_models', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارشات',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='آیدی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('price', models.PositiveBigIntegerField(default=0, verbose_name='قیمت')),
                ('quantity', models.PositiveBigIntegerField(default=1, verbose_name='تعداد')),
                ('weight', models.PositiveBigIntegerField(default=0, verbose_name='وزن')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.productmodel', verbose_name='محصول')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.ordermodel', verbose_name='سفارش')),
            ],
            options={
                'verbose_name': 'آیتم سفارش',
                'verbose_name_plural': 'آیتم سفارشات',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='ordermodel',
            index=models.Index(fields=['-created'], name='orders_orde_created_64675a_idx'),
        ),
        migrations.AddIndex(
            model_name='orderitemmodel',
            index=models.Index(fields=['-created'], name='orders_orde_created_72f60c_idx'),
        ),
    ]
