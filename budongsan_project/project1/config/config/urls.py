"""
URL configuration for budongsan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # 메인(지도)
    path('', views.main), 
    # 좌측 메인 페이지
    path('front/', views.front, name='front'),
    # 좌측 메인 상단 조건 수집 및 예측값 출력
    path('predict/', views.predict, name='predict'),
    # 좌측 메인 페이지 중간 매물 추천 리스트
    path('recommand/', views.recommand, name='recommand'),
    # 좌측 메인 하단 해당 구역 관련 통계 차트 출력
    path('chart/', views.chart, name='chart'),
    # 조건 데이터 리셋
    path('resetFormData/', views.resetdata, name='resetFormData'),
    # 편의시설 마커 찍기
    path('convenient', views.convenient_marker),
    # 어린이 보호구역 차트

]
