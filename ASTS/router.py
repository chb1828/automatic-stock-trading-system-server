from api.viewsets import StockViewset
from rest_framework import routers


router = routers.DefaultRouter()
router.get_api_root_view().cls.__name__ = "ASTS"
router.get_api_root_view().cls.__doc__ = "ASTS Api Service 목록"
router.register('stock',StockViewset)

