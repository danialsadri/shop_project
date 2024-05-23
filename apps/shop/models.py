from apps.utils.models import BaseModel, image_upload_to
from django.db import models


class ProductCategoryModel(BaseModel):
    title = models.CharField(
        max_length=300,
        verbose_name='عنوان'
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        allow_unicode=True,
        verbose_name='اسلاگ'
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'دسته بندی محصول'
        verbose_name_plural = 'دسته بندی  محصول ها'

    def __str__(self):
        return self.title


class ProductModel(BaseModel):
    category = models.ForeignKey(
        to=ProductCategoryModel,
        on_delete=models.CASCADE,
        related_name='product_models',
        verbose_name='دسته بندی'
    )
    title = models.CharField(
        max_length=300,
        verbose_name='عنوان'
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        allow_unicode=True,
        verbose_name='اسلاگ'
    )
    description = models.TextField(
        verbose_name='توضیحات'
    )
    inventory = models.PositiveBigIntegerField(
        default=0,
        verbose_name='موجودی'
    )
    price = models.PositiveBigIntegerField(
        default=0,
        verbose_name='قیمت'
    )
    off = models.PositiveBigIntegerField(
        default=0,
        verbose_name='تخفیف'
    )
    new_price = models.PositiveBigIntegerField(
        default=0,
        verbose_name='قیمت پس از تخفیف'
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'محصول'
        verbose_name_plural = 'محصول ها'

    def __str__(self):
        return self.title


class ProductFeatureModel(BaseModel):
    product = models.ForeignKey(
        to=ProductModel,
        on_delete=models.CASCADE,
        related_name='product_feature_models',
        verbose_name='محصول'
    )
    key = models.CharField(
        max_length=300,
        verbose_name='کلید'
    )
    value = models.CharField(
        max_length=300,
        verbose_name='مقدار'
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی محصول ها'

    def __str__(self):
        return self.key


class ProductImageModel(BaseModel):
    product = models.ForeignKey(
        to=ProductModel,
        on_delete=models.CASCADE,
        related_name='product_image_models',
        verbose_name='محصول'
    )
    file = models.ImageField(
        upload_to=image_upload_to,
        verbose_name='فایل'
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر محصول ها'

    def __str__(self):
        return self.product.title
