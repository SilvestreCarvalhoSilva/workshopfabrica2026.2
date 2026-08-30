
from rest_framework.routers import DefaultRouter

from .views import ProdutoViewSet, CategoriaViewSet


router = DefaultRouter()

router.register(
    'produtos',
    ProdutoViewSet,
    basename='produto'
)

router.register(
    'categorias',
    CategoriaViewSet,
    basename='categoria'
)


urlpatterns = router.urls
