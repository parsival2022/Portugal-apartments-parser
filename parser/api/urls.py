from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('ads_page/<str:extra_arg>/<int:pagination>/', views.ads_page, name='ads_page'),
    path('filter_ads_page/', views.filter_ads_page, name='filter_ads_page'),
    path('filter_ads_page/get_ads_by_type/<int:pagination>/', views.get_ads_by_type, name='get_ads_by_type'),
    path('get_quantity/<int:days>/', views.get_quantity, name='get_quantity'),
    path('get_prices/<int:days>/', views.get_prices, name='get_prices'),
]