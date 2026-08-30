from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (

    ProdutoViewSet,
    CategoriaViewSet,

    
    # Produtos
    lista_produtos,
    detalhe_produto,
    cadastrar_produto,
    editar_produto,
    excluir_produto,
    cadastrar_video,

    # Categorias
    lista_categorias,
    cadastrar_categoria,
    editar_categoria,
    excluir_categoria,

    # Clima
    clima_atual,
    previsao_clima,
    chuva_clima,
    vento_clima,
)

# =========================
# API REST
# =========================

router = DefaultRouter()

router.register(
    r'produtos',
    ProdutoViewSet,
    basename='produto'
)

router.register(
    r'categorias',
    CategoriaViewSet,
    basename='categoria'
)


urlpatterns = [

    # =========================
    # PRODUTOS
    # =========================

    path(
        '',
        lista_produtos,
        name='lista_produtos'
    ),

    path(
        'produtos/',
        lista_produtos,
        name='produtos'
    ),

    path(
        'produto/<int:id>/',
        detalhe_produto,
        name='detalhe_produto'
    ),

    path(
        'produto/cadastrar/',
        cadastrar_produto,
        name='cadastrar_produto'
    ),

    path(
        'produto/<int:id>/editar/',
        editar_produto,
        name='editar_produto'
    ),

    path(
        'produto/<int:id>/excluir/',
        excluir_produto,
        name='excluir_produto'
    ),

    path(
        'produto/<int:id>/video/',
        cadastrar_video,
        name='cadastrar_video'
    ),


    # =========================
    # CLIMA ATUAL
    # =========================

    path(
        'clima/',
        clima_atual,
        name='clima_atual'
    ),


    # =========================
    # PREVISÃO DO CLIMA
    # =========================

    path(
        'previsao-clima/',
        previsao_clima,
        name='previsao_clima'
    ),


    # =========================
    # CHUVA
    # =========================

    path(
        'chuva/',
        chuva_clima,
        name='chuva_clima'
    ),


    # =========================
    # VENTO
    # =========================

    path(
        'vento/',
        vento_clima,
        name='vento_clima'
    ),


    # =========================
    # CATEGORIAS
    # =========================

    path(
        'categorias/',
        lista_categorias,
        name='lista_categorias'
    ),

    path(
        'categorias/cadastrar/',
        cadastrar_categoria,
        name='cadastrar_categoria'
    ),

    path(
        'categorias/<int:id>/editar/',
        editar_categoria,
        name='editar_categoria'
    ),

    path(
        'categorias/<int:id>/excluir/',
        excluir_categoria,
        name='excluir_categoria'
    ),

    path('api/', include(router.urls)),
]


# =========================
# ARQUIVOS DE MÍDIA
# =========================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )