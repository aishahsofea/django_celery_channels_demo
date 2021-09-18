from django.urls import path

from .consumers import CoinListConsumer

ws_urlpatterns = [
    path('coin_list/', CoinListConsumer.as_asgi())
]
