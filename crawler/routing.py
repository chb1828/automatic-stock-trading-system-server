from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'^ws/cs/(?P<room_name>[^/]+)/$', consumer.ClientConsumer.as_asgi()),
]