from .models import Stock
from rest_framework import serializers # This is important

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'name')