import rest_framework.status as status
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .managers import StatisticManager as sm, AdsManager as am
from .permissions import IsAuthenticated


@api_view(['GET', 'POST'])
def home_page(request):
    return render(request, 'home.html')

@api_view(['GET'])
def get_quantity(request, days):
    history = sm.get_quantities_history(days)
    return Response(history, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_prices(request, days):
    history = sm.get_prices_history(days)
    return Response(history, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
def ads_page(request, extra_arg:str, pagination:int):
    if request.method == 'GET':
        return am.get_templated_paginated_ads(request, extra_arg, pagination, template='ads_page.html')
    if request.method == 'POST':
        return am.get_ads_by_type(extra_arg, pagination)



@api_view(['GET'])
def filter_ads_page(request):
    context = {'page': 'Filter ads',
                   'base_page': 'filter_ads_page',
                   'extra': 'get_ads_by_type',
                   'current_pagination': 1,
                   'pagination_length': 0
                   }
    return render(request, 'filter_ads.html', context)
    
@api_view(['POST'])
def get_ads_by_type(request, pagination):
    data = request.data
    type = data['type']
    return am.get_ads_by_type(type, pagination)


