from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    # ALTERADO: Delegação exclusiva da rota raiz para o app churras
    path('', include('churras.urls')),
    path('admin/', admin.site.urls),
]

# Condicional para arquivos de mídia apenas no ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)