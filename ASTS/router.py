from api.viewsets import StockViewset
from rest_framework import routers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import cs.routing


router = routers.DefaultRouter()
router.get_api_root_view().cls.__name__ = "ASTS"
router.get_api_root_view().cls.__doc__ = "ASTS Api Service 목록"
router.register('stock',StockViewset)

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            cs.routing.websocket_urlpatterns
        )
    )
})
