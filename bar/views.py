from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Bar, Stock, Reference
from .serializers import RegisterSerializer, BarListSerializer, StockDetailSerializer, StockListSerializer, \
    ReferenceListSerializer, MenuListSerializer


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class BarViewSet(ModelViewSet):

    permission_classes = []
    serializer_class = BarListSerializer
    queryset = Bar.objects.all()


class ReferenceViewSet(ModelViewSet):

    permission_classes = []
    serializer_class = ReferenceListSerializer
    queryset = Reference.objects.all()


class StockViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = StockListSerializer
    detail_serializer_class = StockDetailSerializer
    lookup_field = 'comptoir'

    def get_queryset(self):
        if 'comptoir' in self.kwargs:
            return Stock.objects.filter(comptoir=self.kwargs['comptoir'])
        else:
            return Stock.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            serializer_class = self.detail_serializer_class
            return serializer_class(*args, **kwargs)
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            Stock.objects.get(reference=request.data['reference'], comptoir=request.data['comptoir'])
            return Response('La référence existe déjà pour ce comptoir')
        except:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        data_to_change = {'stock': request.data.get('stock')}
        stock = Stock.objects.get(reference=request.data['reference'], comptoir=request.data['comptoir'])
        serializer = self.serializer_class(stock, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response(serializer.data)


class RankingViewSet(ModelViewSet):

    pass

    # permission_classes = []
    # serializer_class =


class MenuViewSet(ModelViewSet):

    permission_classes = []
    serializer_class = MenuListSerializer

    def get_queryset(self):
        return Reference.objects.all()
