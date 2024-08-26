import math
from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.response import Response
from .models import Imovirtual, QuantityHistory, PriceHistory, ODIVELAS, AMADORA, LIMIT

class StatisticManager:  
    @classmethod
    def get_average_price_and_length(cls, **kwargs):
        queryset = Imovirtual.objects.filter(**kwargs)
        length = len(queryset)
        price = 0
        price_per_sqm = 0

        for ad in queryset:
            if not ad.price or not ad.price_per_sqm:
                length -= 1
                continue
            price += int(ad.price)
            price_per_sqm += int(ad.price_per_sqm)

        average_price = math.ceil(price / length)
        average_price_per_sqm = math.ceil(price_per_sqm / length)
        return length, average_price, average_price_per_sqm
    
    @classmethod
    def get_average_prices(cls, **kwargs):
        length, avrg_price, avg_price_per_sqm = cls.get_average_price_and_length(**kwargs)
        return {'ads_count': length,
                'average_property_price': avrg_price,
                'average_price_per_sqm': avg_price_per_sqm}
    
    @classmethod
    def combined_get_average_prices(cls):
          amadora_prices = cls.get_average_prices(county=AMADORA)
          odivelas_prices = cls.get_average_prices(county=ODIVELAS)
          prices = {'odivelas_prices': odivelas_prices, 
                    'amadora_prices': amadora_prices,
                    'date': datetime.now().strftime('%Y-%m-%d')}
          return prices
        
    @classmethod
    def get_quantities_history(cls, days):
        days_range = datetime.now() - timedelta(days)
        query = {'date_of_statistic__gte': days_range.strftime('%Y-%m-%d')}
        history = QuantityHistory.get_filtered_history(**query)
        return history
    
    @classmethod
    def get_quantities_history(cls, days):
        days_range = datetime.now() - timedelta(days)
        query = {'date_of_statistic__gte': days_range.strftime('%Y-%m-%d')}
        history = QuantityHistory.get_filtered_history(**query)
        return history
    
    @classmethod
    def get_prices_history(cls, days):
        days_range = datetime.now() - timedelta(days)
        query = {'date_of_statistic__gte': days_range.strftime('%Y-%m-%d')}
        history = PriceHistory.get_filtered_history(**query)
        return history
    
    
class AdsManager:
    ALL_ADS = 'all_ads'
    AMADORA_ADS = AMADORA.casefold()
    ODIVELAS_ADS = ODIVELAS.casefold()
    CHEAPEST = 'cheapest'
    T0 = 'T0'
    T1 = 'T1'
    T2 = 'T2'
    T3 = 'T3'
    T4 = 'T4'

    queries = {
        AMADORA_ADS: {'county': AMADORA},
        ODIVELAS_ADS: {'county': ODIVELAS},
        ALL_ADS: {'no_filter': True},
        CHEAPEST: {'price_per_sqm__lt': 2500, 'order_by': 'price_per_sqm'},
        T0: {'title__icontains': T0},
        T1: {'title__icontains': T1},
        T2: {'title__icontains': T2},
        T3: {'title__icontains': T3},
        T4: {'title__icontains': T4},
    }

    @classmethod
    def get_templated_paginated_ads(cls, request, extra_page:str, pagination, template=None):
        skip = LIMIT * (pagination - 1)
        query = cls.queries[extra_page]
        ads, pagination_length = Imovirtual.get_paginated_ads(skip, **query)
        if not ads:
            context = {'msg': 'No ads was found!'}
            return render(request, template, context)
        context = {'ads': ads, 
                       'base_page': 'ads_page',
                       'extra': extra_page, 
                       'page': extra_page.replace('_', ' ').capitalize(), 
                       'current_pagination': pagination,
                       'pagination_length': pagination_length}
        return render(request, template, context, status=200)
    
    @classmethod
    def get_paginated_ads(cls, page, pagination):
        skip = LIMIT * (pagination - 1)
        query = cls.queries[page]
        ads, pagination_length = Imovirtual.get_paginated_ads(skip, **query)
        if not ads:
            data = {'msg': 'No ads was found!'}
        data = {'ads': ads, 
                       'base_page': 'ads_page',
                       'extra': page, 
                       'page': 'All ads', 
                       'current_pagination': pagination,
                       'pagination_length': pagination_length}
        return Response(data=data)
    
    @classmethod
    def get_ads_by_type(cls, type, pagination):
        skip = LIMIT * (pagination - 1)
        query = cls.queries[type]
        ads, pagination_length = Imovirtual.get_paginated_ads(skip, **query)
        data = {'ads': ads,
                'current_pagination': pagination,
                'pagination_length': pagination_length}
        return Response(data=data)


    @classmethod
    def create_and_save_history(cls):
        prices = StatisticManager.combined_get_average_prices()
        odivelas_count, odivelas_price, odivelas_price_per_sqm = prices['odivelas_prices'].values()
        amadora_count, amadora_price, amadora_price_per_sqm = prices['amadora_prices'].values()
        current_data = prices['date']
        quantity_obj = {'date_of_statistic': current_data,
                        'amadora_quantity': amadora_count,
                        'odivelas_quantity': odivelas_count}
        price_obj = {'date_of_statistic': current_data,
                     'amadora_avg_property_price': amadora_price,
                     'amadora_avg_price_per_sqm': amadora_price_per_sqm,
                     'odivelas_avg_property_price': odivelas_price,
                     'odivelas_avg_price_per_sqm': odivelas_price_per_sqm
                     }
        q_result = QuantityHistory.objects.create(**quantity_obj)
        p_result = PriceHistory.objects.create(**price_obj)

        return q_result and p_result
