from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import AnalystRatingSerializer
from .models import AnalystRating
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
import os
import json

class TradingView(viewsets.ModelViewSet):      
    serializer_class = AnalystRatingSerializer
    queryset = AnalystRating.objects.all()     


class Assets(View):

    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'static', filename)

        if os.path.isfile(path):
            with open(path, 'rb') as file:
                return HttpResponse(file.read(), content_type='application/javascript')
        else:
            return HttpResponseNotFound()     

@api_view(['GET', 'POST'])
def analyst_ratings(request):

    if request.method == 'POST':
        ratings = json.loads(request.data)
        for rating in ratings:

            serializer = AnalystRatingSerializer(data=rating)

            if serializer.is_valid():
                serializer.save()
        
        return HttpResponse("Worked",status=201)

    if request.method == 'GET':
        instance = AnalystRating.objects.order_by('date').last()
        return HttpResponse(instance,status=201)