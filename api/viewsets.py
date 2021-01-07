from rest_framework import viewsets
from . import models
from . import serializers


class StockViewset(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer

