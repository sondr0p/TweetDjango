from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('', consumers.myConsumer),
    path('search/', consumers.myConsumer),
]