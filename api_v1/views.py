from django.shortcuts import render

# Create your views here.
from rest_framework import views, status
from rest_framework.response import Response

from analytics.models import Ticker_Minute_USD_JPY


class RealCandleAPIView(views.APIView):
    def get(self, request):
        prev = int(request.GET.get('position'))
        next = 40 + prev

        candle_data = list(map(lambda x: x.to_array(), Ticker_Minute_USD_JPY.objects.all().order_by('-id')[prev:next]))
        candle_data.reverse()
        return Response({"data": candle_data}, status.HTTP_200_OK)