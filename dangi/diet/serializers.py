# diet/serializers.py
from rest_framework import serializers
from .models import Diet, DailyDiet, Food

class DailyDietSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyDiet
        fields = '__all__'
class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        model = Diet
        fields = '__all__'


class FoodInfoSerializer(serializers.ModelSerializer):
    food_seq = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    kcal = serializers.IntegerField()
    carbo = serializers.IntegerField()
    protein = serializers.IntegerField()
    prov = serializers.IntegerField()

    class Meta:
        model = Food
        fields = ['food_seq','name', 'quantity', 'kcal', 'carbo', 'protein', 'prov']
