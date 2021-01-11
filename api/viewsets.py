from rest_framework.response import Response
from rest_framework import viewsets, status
from . import models, serializers


class StockViewset(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer

    def create(self, request, *args, **kwargs):
        stock_data = request.data.get("data")
        auth = request.META.get('HTTP_AUTHENTICATION')
        if(auth!="ff35885ab6c63290ccdf60b80a9b37769e287ec5"):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=stock_data,many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)

    def perform_create(self, serializer):
        serializer.save()