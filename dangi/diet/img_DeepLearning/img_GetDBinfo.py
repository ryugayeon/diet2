# 식품영양 DB에서 음식명 읽어옴
from diet.serializers import Food, FoodInfoSerializer

class FoodInfoChecker:
    def __init__(self, foodmenu, quantity_level):
        self.foodmenu = foodmenu
        self.quantity_level = quantity_level

    def get_nutrition_info(self):
        # foodmenu와 일치하는 행 가져옴
        try:
            model = Food.objects.get(name = self.foodmenu)
        except Exception as e:
            foodname = None
            quantity = None
            kcal = None
            carbo = None
            protein = None
            prov = None
            error = e
            return foodname, quantity, kcal, carbo, protein, prov, error

        serializer = FoodInfoSerializer(model)

        # 각 feature들 가져오기 + quantity level에 곱해서
        foodname = str(serializer.data['name'])
        quantity = int(serializer.data['quantity'] * self.quantity_level)
        kcal = int(serializer.data['kcal'] * self.quantity_level)
        carbo = int(serializer.data['carbo'] * self.quantity_level)
        protein = int(serializer.data['protein'] * self.quantity_level)
        prov = int(serializer.data['prov'] * self.quantity_level)

        error = False

        # # db연동 전 임시 값들.
        # quantity = 375
        # kcal = 300
        # carbo = 23.5
        # protein = 21.2
        # prov = 11.5

        return foodname, quantity, kcal, carbo, protein, prov, error