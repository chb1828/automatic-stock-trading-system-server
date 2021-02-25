from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'^ws/client/test', consumer.ClientConsumer.as_asgi()),
]