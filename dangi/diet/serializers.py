# diet/serializers.py
from rest_framework import serializers
from .models import Diet
from .models import DailyDiet

class DailyDietSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyDiet
        fields = '__all__'
class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'
