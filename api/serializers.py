from .models import AnalystRating
from rest_framework import serializers # This is important
from rest_framework.validators import UniqueTogetherValidator

class AnalystRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalystRating
        fields = ('date','ticker','company','action','brokerage','current','target_original','target_new','rating','impact','percent_upside')
        validators = [
            UniqueTogetherValidator(
                queryset=AnalystRating.objects.all(),
                fields=['date','ticker','company','action','brokerage','current','target_original','target_new','rating','impact','percent_upside']
            )
        ]