from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls', namespace='home')),
    path('shop/', include('apps.shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.sites.AdminSite.site_header = 'پنل مدیریت'
admin.sites.AdminSite.site_title = 'پنل مدیریت'
admin.sites.AdminSite.index_title = 'پنل مدیریت'
