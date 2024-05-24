from django.db import models
from django.http import Http404


class BaseModel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='آیدی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True

    def update(self, **kwargs):
        for field in kwargs:
            self.__setattr__(field, kwargs[field])
        self.save()

    @classmethod
    def get_object_or_404(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            raise Http404

    @classmethod
    def is_exist(cls, *args, **kwargs):
        obj = cls.objects.filter(*args, **kwargs)
        return obj.exists(), obj.first()
