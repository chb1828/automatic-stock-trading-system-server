from rest_framework.response import Response
from rest_framework import viewsets, status

from util import setEnvironment
from . import models, serializers


class StockViewset(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer

    def create(self, request, *args, **kwargs):
        stock_data = request.data.get("data")
        auth = request.META.get('HTTP_AUTHENTICATION')       # 헤더에서 값을 가져옴
        api_key = setEnvironment.get_secret("API_AUTH_KEY")
        if auth != api_key:  # secrets.json 에서 토큰값 비교
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=stock_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
