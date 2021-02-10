from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StockSerializer
from .models import Stock
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
import os

class TradingView(viewsets.ModelViewSet):      
    serializer_class = StockSerializer
    queryset = Stock.objects.all()     


class Assets(View):

    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'static', filename)

        if os.path.isfile(path):
            with open(path, 'rb') as file:
                return HttpResponse(file.read(), content_type='application/javascript')
        else:
            return HttpResponseNotFound()        
