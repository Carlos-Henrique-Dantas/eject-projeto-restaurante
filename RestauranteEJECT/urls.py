"""
URL configuration for RestauranteEJECT project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # O segredo está aqui: aspas vazias '' significam a raiz do site (localhost:8000/)
    path('', include('RestauranteAPOLLO.urls')),
]

# Deixe APENAS a configuração de MEDIA aqui. O Django carrega o STATIC sozinho!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)