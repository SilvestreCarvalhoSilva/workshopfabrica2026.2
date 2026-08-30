
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    # =========================
    # PÁGINAS DO SISTEMA
    # =========================

    path(
        '',
        include('produtos.urls')
    ),

    # =========================
    # API
    # =========================

    path(
        'api/',
        include('produtos.api_urls')
    ),

]


# =========================
# ARQUIVOS DE MÍDIA
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

