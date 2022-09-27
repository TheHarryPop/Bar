from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_multiple_model.views import FlatMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from collections import OrderedDict

from .models import User, Bar, Stock, Reference, Order
from .serializers import RegisterSerializer, BarListSerializer, StockDetailSerializer, StockListSerializer, \
    ReferenceListSerializer, MenuListSerializer, OrderSerializer, OrderItemsSerializer, RankingAllSerializer, \
    RankingMissSerializer, RankingBestSerializer


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class BarViewSet(ModelViewSet):

    # permission_classes = [IsAuthenticated]
    serializer_class = BarListSerializer
    queryset = Bar.objects.all()


class ReferenceViewSet(ModelViewSet):

    # permission_classes = [IsAuthenticated]
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

        except ObjectDoesNotExist:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        data_to_change = {'stock': request.data.get('stock')}
        try:
            stock = Stock.objects.get(reference=request.data['reference'], comptoir=self.kwargs['comptoir'])
            serializer = self.serializer_class(stock, data=data_to_change, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('Merci de créer la référence pour ce comptoir avant de mettre à jour les stocks')


class FormatResponse(MultipleModelLimitOffsetPagination):

    def format_response(self, data):
        return data


class RankingViewSet(FlatMultipleModelAPIView):

    # permission_classes = [IsAuthenticated]
    pagination_class = FormatResponse
    add_model_type = None

    def get_querylist(self):
        query = [Bar.objects.all()[0]]
        if 'orders' in self.request.get_full_path():
            querylist = [{'queryset': query, 'serializer_class': RankingBestSerializer}]

        else:
            querylist = [{'queryset': query, 'serializer_class': RankingAllSerializer}, {'queryset': query,
                                                                                         'serializer_class':
                                                                                             RankingMissSerializer}]
        return querylist


class MenuViewSet(ModelViewSet):

    permission_classes = []
    serializer_class = MenuListSerializer

    def get_queryset(self):
        return Reference.objects.all()


class OrderViewSet(ModelViewSet):

    permission_classes = []
    serializer_class = OrderSerializer
    post_serializer_class = OrderItemsSerializer

    def get_queryset(self):
        return Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={'comptoir': self.kwargs['pk']})
        bar = Bar.objects.get(id=self.kwargs['pk'])
        serializer.is_valid()
        order = serializer.save(comptoir=bar)

        for item in request.data['items']:
            ref = Reference.objects.get(ref=item['ref'])
            serializer_item = self.post_serializer_class(data=item)
            serializer_item.is_valid()
            serializer_item.save(item=ref, order=order)
            stock = Stock.objects.get(reference=ref, comptoir=self.kwargs['pk'])
            stock.stock -= 1
            stock.save()

        return Response(serializer.data)
