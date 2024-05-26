# Generated by Django 5.0.6 on 2024-05-26 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='آیدی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, max_length=300, unique=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'دسته بندی محصول',
                'verbose_name_plural': 'دسته بندی  محصول ها',
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['-created'], name='shop_produc_created_333be4_idx')],
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='آیدی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, max_length=300, unique=True, verbose_name='اسلاگ')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('inventory', models.PositiveBigIntegerField(default=0, verbose_name='موجودی')),
                ('price', models.PositiveBigIntegerField(default=0, verbose_name='قیمت')),
                ('off', models.PositiveBigIntegerField(default=0, verbose_name='تخفیف')),
                ('new_price', models.PositiveBigIntegerField(default=0, verbose_name='قیمت پس از تخفیف')),
                ('weight', models.PositiveBigIntegerField(default=0, verbose_name='وزن')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_models', to='shop.productcategorymodel', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصول ها',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ProductImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='آیدی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('file', models.ImageField(upload_to='product_image/', verbose_name='فایل')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image_models', to='shop.productmodel', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'تصویر محصول',
                'verbose_name_plural': 'تصویر محصول ها',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ProductFeatureModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='آیدی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('key', models.CharField(max_length=300, verbose_name='کلید')),
                ('value', models.CharField(max_length=300, verbose_name='مقدار')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_feature_models', to='shop.productmodel', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'ویژگی محصول',
                'verbose_name_plural': 'ویژگی محصول ها',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='productmodel',
            index=models.Index(fields=['title'], name='shop_produc_title_b5ffda_idx'),
        ),
        migrations.AddIndex(
            model_name='productmodel',
            index=models.Index(fields=['id', 'slug'], name='shop_produc_id_c4056b_idx'),
        ),
        migrations.AddIndex(
            model_name='productmodel',
            index=models.Index(fields=['-created'], name='shop_produc_created_c83a4f_idx'),
        ),
        migrations.AddIndex(
            model_name='productimagemodel',
            index=models.Index(fields=['-created'], name='shop_produc_created_39af30_idx'),
        ),
        migrations.AddIndex(
            model_name='productfeaturemodel',
            index=models.Index(fields=['-created'], name='shop_produc_created_77b2f4_idx'),
        ),
    ]
