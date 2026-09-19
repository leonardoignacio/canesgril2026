from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from churras.views import index

urlpatterns = [
    path('', index, name='home'),
    path('', include('churras.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

