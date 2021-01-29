from django.urls import path
from django.urls import re_path, path
from . import consumers
from analytics.views import top

app_name = "analytics"

urlpatterns = [
    path('', top)
]

websocket_urlpatterns = [
    re_path('ws/chat/(?P<room_name>[^/]+)/', consumers.ChatConsumer),
    path("ws/notifications/<str:product_code>/", consumers.NotificationConsumer, name="ws_notifications")
]
