from dateutil import parser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from util import setEnvironment
from . import models, serializers
from .models import Stock


class StockViewset(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer

    @action(detail=False, methods=['POST'], name='bulk save')
    def bulk(self, request, *args, **kwargs):
        auth = request.META.get('HTTP_AUTHENTICATION')
        api_key = setEnvironment.get_secret("API_AUTH_KEY")
        if auth != api_key:
            response_data = {'message': '인증이 실패했습니다', 'status': 'status.HTTP_401_UNAUTHORIZED'}
            return Response(response_data,status=status.HTTP_401_UNAUTHORIZED)
        stock_data = request.data.get("data")
        self.validate_stock(stock_data)
        response_data = {'message': '저장이 성공했습니다', 'data': stock_data, 'status': 'success'}
        headers = self.get_success_headers(response_data)
        Stock.objects.all()
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def validate_stock(self, realData):
        data = [Stock(**stock) for stock in realData]
        for item in data:
            date = parser.parse(item.listedDate)
            item.listedDate = date
        Stock.objects.bulk_update_or_create(data,['name', 'cnt', 'construction', 'listedDate', 'lastPrice', 'state'], match_field='code')