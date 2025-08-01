from django.contrib import admin
from django.urls import path, include

# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('django.contrib.auth.urls')),
    path('store/', include('store.urls', namespace="store")),
    path('', include('public.urls', namespace='public')),
    path('', include('storelite.urls', namespace="storelite")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)