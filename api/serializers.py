from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    listedDate = serializers.DateTimeField(format="%Y-%m-%d",input_formats=['%Y%m%d'])

    class Meta:
        model = Stock
        fields = '__all__'
