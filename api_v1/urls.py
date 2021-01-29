from django.urls import path

from analytics.views import top
from api_v1.views import RealCandleAPIView

app_name = "api_v1"

urlpatterns = [
    path('real_candle/', RealCandleAPIView.as_view(), name="get_real_candle"),
]
