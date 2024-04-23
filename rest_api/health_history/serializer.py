from rest_framework import serializers
from .models import HealthHistory

class HealthHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthHistory
        fields = ['user','diabetics_score','weight','calories', 'carbs', 'fat', 'proteins']