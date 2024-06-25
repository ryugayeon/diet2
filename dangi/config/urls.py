"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import UserMemberView, CheckUserId, UserLogin, UserHeight, UserLogout, UserDeactivate, DietPeriodView, DietRecommendationView
from diet.views import DietMealsView, DietByDateView, DailyDietByDateView, DailyDietByDateRangeView, DailyDietKcalDifferenceView


urlpatterns = [
    path('admin/', admin.site.urls), # 이걸로 들어가야 내용 확인 가능
    # path('api-auth/', include('rest_framework.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # User URLS
    path('user/member/', UserMemberView.as_view(), name='user_member'),  # 회원가입 및 사용자 정보 조회
    path('user/member/<str:user_id>/', CheckUserId.as_view(), name='check_user_id'), #아이디 중복 체크
    path('user/login/', UserLogin.as_view(), name='user_login'), #로그인
    path('user/logout/', UserLogout.as_view(), name='user_logout'),  # 로그아웃
    path('user/delete/', UserDeactivate.as_view(), name='user_delete'),  # 회원탈퇴
    path('user/diet_height/', UserHeight.as_view(), name='user_detail'),  # 다이어트 정보 입력 확인 [height 값 체크]
    path('user/diet_info/', DietPeriodView.as_view(), name='diet_period'),  # 다이어트 기간 정보 조회 및 업데이트
    path('user/diet_info/recommend_period/', DietRecommendationView.as_view(), name='diet_recommendation'),  # 다이어트 추천 기간 조회

    #Diet URLS
    path('diet/meals/', DietMealsView.as_view(), name='diet_record'), #식단 기록
    path('diet/meals/<int:pk>/', DietMealsView.as_view(), name='diet_meals_update'), #식단 기록 수정 및 삭제
    path('diet/meals/by-date/', DietByDateView.as_view(), name='diet_by_date'), #지정날짜의 식단 리스트 조회
    path('diet/daily_meals/by-date/', DailyDietByDateView.as_view(), name='daily_diet_by_date'), #지정날짜의 일일 섭취량 조회
    path('diet/daily_meals/period/', DailyDietByDateRangeView.as_view(), name='daily_diet_by_date_range'), #시작일, 마지막일 기간동안의 일일섭취량 조회
    path('diet/progress/', DailyDietKcalDifferenceView.as_view(), name='daily_diet_kcal_difference'), #현재까지의 소모 칼로리 조회
]
