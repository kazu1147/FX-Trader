from django.shortcuts import render


# Create your views here.
from constants import HOST, PORT


def top(request):
    if request.method == "GET":
        contexts = {
            'sidebar_equipment': True,
            'host': HOST,
            'port': PORT,
        }
        return render(request, 'analytics/top.html', contexts)