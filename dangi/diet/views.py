# diet/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Diet, DailyDiet
from .serializers import DietSerializer, DailyDietSerializer
from user.models import User
from user.models import DietPeriod
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class DietMealsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user  # 토큰 인증을 통해 얻은 사용자
        user_seq = user.user_seq

        # diet_period의 tdee 값을 가져오기
        diet_period = DietPeriod.objects.filter(user_seq=user).order_by('-start_dt').first()
        if not diet_period:
            return Response({'error': 'Diet period not found'}, status=status.HTTP_404_NOT_FOUND)
        tdee = diet_period.tdee

        data = request.data
        date_str = data.get('date')
        date_obj = parse_datetime(date_str)

        if not date_obj:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # 동일한 user_seq 번호를 갖는 daily_diet 찾기 또는 생성
        daily_diet, created = DailyDiet.objects.get_or_create(
            user_seq=user,
            date__date=date_obj.date(),
            defaults={
                'kcal': data.get('kcal'),
                'carbo': data.get('carbo'),
                'protein': data.get('protein'),
                'prov': data.get('prov'),
                'date': date_obj,
                'success_yn': 'N',  # 기본값 설정
            }
        )

        if not created:
            # 동일한 날짜에 대한 daily_diet이 이미 존재하면 업데이트
            daily_diet.kcal += data.get('kcal', 0)
            daily_diet.carbo += data.get('carbo', 0)
            daily_diet.protein += data.get('protein', 0)
            daily_diet.prov += data.get('prov', 0)

        # success_yn 업데이트
        daily_diet.success_yn = 'Y' if daily_diet.kcal < tdee else 'N'
        daily_diet.save()

        # Diet 레코드 생성
        diet_data = {
            'daily_diet_seq': daily_diet.daily_diet_seq,
            'user_seq': user_seq,
            'name': data.get('name'),
            'quantity': data.get('quantity'),
            'kcal': data.get('kcal'),
            'carbo': data.get('carbo'),
            'protein': data.get('protein'),
            'prov': data.get('prov'),
            'date': date_obj,
            'food_img': data.get('food_img', None),
        }

        serializer = DietSerializer(data=diet_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            diet = Diet.objects.get(pk=pk)
        except Diet.DoesNotExist:
            return Response({'error': 'Diet not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # 이전 daily_diet의 값을 원래대로 되돌림
        previous_daily_diet = diet.daily_diet_seq

        # 현재 값들을 저장해둠
        original_kcal = diet.kcal
        original_carbo = diet.carbo
        original_protein = diet.protein
        original_prov = diet.prov

        # 저장 전 daily_diet에서 기존 값 빼기
        previous_daily_diet.kcal -= original_kcal
        previous_daily_diet.carbo -= original_carbo
        previous_daily_diet.protein -= original_protein
        previous_daily_diet.prov -= original_prov
        previous_daily_diet.save()

        # diet 값 업데이트
        diet.name = data.get('name', diet.name)
        diet.quantity = data.get('quantity', diet.quantity)
        diet.kcal = data.get('kcal', diet.kcal)
        diet.carbo = data.get('carbo', diet.carbo)
        diet.protein = data.get('protein', diet.protein)
        diet.prov = data.get('prov', diet.prov)
        date_str = data.get('date', diet.date)
        diet.date = parse_datetime(date_str) if date_str != diet.date else diet.date
        diet.food_img = data.get('food_img', diet.food_img)

        # 동일한 user_seq 번호를 갖는 daily_diet 찾기 또는 생성
        daily_diet, created = DailyDiet.objects.get_or_create(
            user_seq=diet.user_seq,
            date__date=diet.date.date(),
            defaults={
                'kcal': diet.kcal,
                'carbo': diet.carbo,
                'protein': diet.protein,
                'prov': diet.prov,
                'date': diet.date,
                'success_yn': 'N',  # 기본값 설정
            }
        )

        if not created:
            # 새로운 daily_diet에 값 추가
            daily_diet.kcal += diet.kcal
            daily_diet.carbo += diet.carbo
            daily_diet.protein += diet.protein
            daily_diet.prov += diet.prov

        # success_yn 업데이트
        diet_period = DietPeriod.objects.filter(user_seq=diet.user_seq).order_by('-start_dt').first()
        if not diet_period:
            return Response({'error': 'Diet period not found'}, status=status.HTTP_404_NOT_FOUND)
        tdee = diet_period.tdee
        daily_diet.success_yn = 'Y' if daily_diet.kcal < tdee else 'N'
        daily_diet.save()

        # diet 값 저장
        diet.daily_diet_seq = daily_diet
        diet.save()

        serializer = DietSerializer(diet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            diet = Diet.objects.get(pk=pk)
        except Diet.DoesNotExist:
            return Response({'error': '식사를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 이전 daily_diet의 값을 원래대로 되돌림
        previous_daily_diet = diet.daily_diet_seq

        # diet 값 삭제 전 daily_diet에서 기존 값 빼기
        previous_daily_diet.kcal -= diet.kcal
        previous_daily_diet.carbo -= diet.carbo
        previous_daily_diet.protein -= diet.protein
        previous_daily_diet.prov -= diet.prov

        # success_yn 업데이트
        diet_period = DietPeriod.objects.filter(user_seq=diet.user_seq).order_by('-start_dt').first()
        if not diet_period:
            return Response({'error': 'Diet period not found'}, status=status.HTTP_404_NOT_FOUND)
        tdee = diet_period.tdee
        previous_daily_diet.success_yn = 'Y' if previous_daily_diet.kcal < tdee else 'N'
        previous_daily_diet.save()

        # Diet 레코드 삭제
        diet.delete()

        return Response({'message': '식사가 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

class DietByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'Date parameter를 입력해주세요'}, status=status.HTTP_400_BAD_REQUEST)

        date_obj = parse_datetime(date_str)
        if not date_obj:
            return Response({'error': 'date format이 잘못되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 특정 날짜와 일치하는 diet 레코드 찾기
        diets = Diet.objects.filter(date__date=date_obj.date())

        if not diets.exists():
            return Response({'error': '해당 날짜의 식사가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DietSerializer(diets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DailyDietByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        date_obj = parse_datetime(date_str)
        if not date_obj:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # 특정 날짜와 일치하는 daily_diet 레코드 찾기
        daily_diets = DailyDiet.objects.filter(date__date=date_obj.date())

        if not daily_diets.exists():
            return Response({'error': 'No daily_diets found for the specified date'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = DailyDietSerializer(daily_diets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DailyDietByDateRangeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not start_date_str or not end_date_str:
            return Response({'error': 'Both start_date and end_date parameters are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_datetime(start_date_str)
        end_date = parse_datetime(end_date_str)

        if not start_date or not end_date:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # 날짜의 연월일만 비교하여 해당 기간 내의 daily_diet 레코드 찾기
        daily_diets = DailyDiet.objects.filter(
            date__date__gte=start_date.date(),
            date__date__lte=end_date.date()
        ).order_by('date')

        if not daily_diets.exists():
            return Response({'error': 'No daily_diets found for the specified date range'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = DailyDietSerializer(daily_diets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DailyDietKcalDifferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # 토큰 인증을 통해 얻은 사용자

        # 사용자의 현재 다이어트 기간 가져오기
        diet_period = DietPeriod.objects.filter(user_seq=user).order_by('-start_dt').first()
        if not diet_period:
            return Response({'error': 'Diet period not found'}, status=status.HTTP_404_NOT_FOUND)

        daily_kcal = diet_period.tdee

        # 사용자의 모든 daily_diet 레코드 가져오기
        daily_diets = DailyDiet.objects.filter(user_seq=user)
        # print(daily_diets)

        # daily_kcal - daily_diet의 kcal 값들의 합 계산
        kcal_difference_sum = sum(daily_kcal - diet.kcal for diet in daily_diets)
        # print("칼로리 추이:", kcal_difference_sum)

        # 합이 음수라면 0으로 설정
        if kcal_difference_sum < 0:
            kcal_difference_sum = 0

        return Response({'kcal_difference_sum': kcal_difference_sum}, status=status.HTTP_200_OK)