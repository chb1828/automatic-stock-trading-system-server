from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import viewsets, status

from util import setEnvironment
from . import models, serializers


class StockViewset(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer

    @action(detail=False, methods=['POST'], name='bulk save')
    def bulk(self, request, *args, **kwargs):
        auth = request.META.get('HTTP_AUTHENTICATION')
        api_key = setEnvironment.get_secret("API_AUTH_KEY")
        if auth != api_key:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        stock_data = request.data.get("data")
        serializer = self.get_serializer(data=stock_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)  # result 값을 custom json 형식의 포맷으로 전송한다 .
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
