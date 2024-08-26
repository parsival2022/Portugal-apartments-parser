from rest_framework.serializers import ModelSerializer
from .models import Imovirtual

class ImovirtualSerializer(ModelSerializer):
    class Meta:
        model = Imovirtual
        fields = '__all__'
    

