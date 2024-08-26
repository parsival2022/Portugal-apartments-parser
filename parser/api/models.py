import math
from django.db import models

ODIVELAS = 'Odivelas'
AMADORA = 'Amadora'
LIMIT = 20

class Imovirtual(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_of_extraction = models.CharField(max_length=50)
    extracted_from = models.CharField(max_length=50)
    ad_url = models.URLField()
    title = models.CharField(max_length=255)
    market_type = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    advert_type = models.CharField(max_length=20)
    features = models.TextField(blank=True, default='')
    area = models.CharField(max_length=10)
    gross_area = models.CharField(max_length=18, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    property_type = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=100)
    owner_phones = models.CharField(max_length=200)
    agency_name = models.CharField(max_length=100)
    agency_phones = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    coordinates_latitude = models.FloatField(null=True)
    coordinates_longitude = models.FloatField(null=True)
    bathrooms = models.IntegerField(null=True)
    rooms = models.IntegerField(null=True)
    condition = models.CharField(max_length=20, null=True)
    energy_certificate = models.CharField(max_length=20, null=True)

    @classmethod
    def get_ad(cls, **kwargs):
        try:
            ad = cls.objects.get(**kwargs)
            return ad
        except cls.DoesNotExist:
            return None
        
    @classmethod
    def get_ad_by_url(cls, url):
        query = {'ad_url': url}
        return cls.get_ad(**query)
           
    @classmethod
    def charfield_keys(cls):
        charfield_keys = (field.name for field in cls._meta.fields if isinstance(field, models.CharField))
        return charfield_keys
    
    @classmethod
    def get_sorted_ads(cls):
        queryset = cls.objects.all().order_by('price')
        return [ad.get_property_info() for ad in queryset]
    
    @classmethod
    def get_filtered_ads(cls, **kwargs):
        if 'order_by' in kwargs:
            order_by = kwargs.pop('order_by')
        else: 
            order_by = 'price'
        queryset = cls.objects.filter(**kwargs).order_by(order_by)
        return [ad.get_property_info() for ad in queryset]
    
    @classmethod
    def get_paginated_ads(cls, skip, **kwargs):
        if 'no_filter' in kwargs :
           ads = cls.get_sorted_ads()
        else:
            ads = cls.get_filtered_ads(**kwargs)
        pagination_length = math.ceil(len(ads) / LIMIT)
        limited_articles = ads[skip:skip+LIMIT]
        return limited_articles, pagination_length

    def get_price(self):
        return f"{self.price} €"
    
    def get_price_per_sqm(self):
        return f"{self.price_per_sqm} € per square meter"
        
    def get_property_info(self):
        return {
            'title': self.title,
            'url': self.ad_url,
            'property_type': self.property_type.capitalize(),
            'condition': self.condition.capitalize(),
            'description': self.description,
            'area': self.area,
            'gross_area': self.gross_area,
            'bathrooms': self.bathrooms,
            'rooms': self.rooms,
            'features': self.features,
            'energy_certificate': self.energy_certificate.title(),
            'price': f"{self.price} €" if self.price not in (None, 'Not provided') else self.price,
            'price_per_sqm': f"{self.price_per_sqm} €" if self.price_per_sqm not in (None, 'Not provided') else self.price_per_sqm,
            'city': self.city,
            'county': self.county,
        }
    
class QuantityHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_of_statistic = models.CharField(max_length=50)
    amadora_quantity = models.IntegerField(null=True)
    odivelas_quantity = models.IntegerField(null=True)

    @classmethod
    def get_history(cls):
        queryset = cls.objects.all()
        return [row.get_row_info() for row in queryset]
    
    @classmethod
    def get_filtered_history(cls, **kwargs):
        queryset = cls.objects.filter(**kwargs)
        return [row.get_row_info() for row in queryset]
    
    def get_row_info(self):
        return {'date': self.date_of_statistic,
                'amadora': self.amadora_quantity,
                'odivelas': self.odivelas_quantity
                }
    
class PriceHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_of_statistic = models.CharField(max_length=50)
    amadora_avg_property_price = models.IntegerField(null=True)
    odivelas_avg_property_price = models.IntegerField(null=True)
    amadora_avg_price_per_sqm = models.IntegerField(null=True)
    odivelas_avg_price_per_sqm = models.IntegerField(null=True)

    @classmethod
    def get_history(cls):
        queryset = cls.objects.all()
        return [row.get_row_info() for row in queryset]
    
    @classmethod
    def get_filtered_history(cls, **kwargs):
        queryset = cls.objects.filter(**kwargs)
        return [row.get_row_info() for row in queryset]
    
    def get_row_info(self):
        return {'date': self.date_of_statistic,
                'amadora_property_price': self.amadora_avg_property_price,
                'amadora_price_per_sqm': self.amadora_avg_price_per_sqm,
                'odivelas_property_price': self.odivelas_avg_property_price,
                'odivelas_price_per_sqm': self.odivelas_avg_price_per_sqm
                }
    


    

