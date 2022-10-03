from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_multiple_model.views import FlatMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from django_filters import rest_framework as filters

from .models import User, Bar, Stock, Reference, Order
from .serializers import RegisterSerializer, BarListSerializer, StockDetailSerializer, StockListSerializer, \
    ReferenceListSerializer, MenuListSerializer, MenuDetailSerializer, OrderSerializer, OrderItemsSerializer, \
    RankingAllSerializer, RankingMissSerializer, RankingBestSerializer
from .permissions import BarPermissions, ReferencesPermissions, OrderPermissions


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class BarViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, BarPermissions]
    serializer_class = BarListSerializer
    queryset = Bar.objects.all()


class ReferenceViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, ReferencesPermissions]
    serializer_class = ReferenceListSerializer
    queryset = Reference.objects.all()


class StockViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StockListSerializer
    detail_serializer_class = StockDetailSerializer
    queryset = Stock.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            Stock.objects.get(reference=request.data['reference'], comptoir=self.kwargs['pk'])
            return Response('La référence existe déjà pour ce comptoir')

        except ObjectDoesNotExist:
            bar = Bar.objects.get(id=self.kwargs['pk'])
            serializer.is_valid()
            serializer.save(comptoir=bar)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = Stock.objects.filter(comptoir=self.kwargs['pk'])
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data_to_change = {'stock': request.data.get('stock')}
        try:
            stock = Stock.objects.get(reference=request.data['reference'], comptoir=self.kwargs['pk'])
            serializer = self.serializer_class(stock, data=data_to_change, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response('Merci de créer la référence pour ce comptoir avant de mettre à jour les stocks')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class FormatResponse(MultipleModelLimitOffsetPagination):

    def format_response(self, data):
        return data


class RankingViewSet(FlatMultipleModelAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = FormatResponse
    add_model_type = None

    def get_querylist(self):
        query = [Bar.objects.all()[0]]
        if 'orders' in self.request.get_full_path():
            querylist = [{'queryset': query, 'serializer_class': RankingBestSerializer}]
        else:
            querylist = [{'queryset': query, 'serializer_class': RankingAllSerializer},
                         {'queryset': query, 'serializer_class': RankingMissSerializer}]
        return querylist


class MenuViewSet(ModelViewSet):

    permission_classes = []
    serializer_class = MenuListSerializer
    detail_serializer_class = MenuDetailSerializer
    queryset = Reference.objects.all()
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('availability', )

    def retrieve(self, request, *args, **kwargs):
        instance = Reference.objects.filter(stock_reference__comptoir=self.kwargs['pk'])
        bar = Bar.objects.get(id=kwargs['pk'])
        serializer = MenuDetailSerializer(instance, context={'bar': bar}, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class OrderViewSet(ModelViewSet):

    permission_classes = [OrderPermissions]
    serializer_class = OrderSerializer
    post_serializer_class = OrderItemsSerializer

    def get_queryset(self):
        return Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={'comptoir': self.kwargs['pk']})
        bar = Bar.objects.get(id=self.kwargs['pk'])
        serializer.is_valid()
        order = serializer.save(comptoir=bar)

        messages = []

        for item in request.data['items']:
            ref = Reference.objects.get(ref=item['ref'])
            serializer_item = self.post_serializer_class(data=item)
            serializer_item.is_valid()
            serializer_item.save(item=ref, order=order)
            stock = Stock.objects.get(reference=ref, comptoir=self.kwargs['pk'])
            if (stock.stock - 1) < 2:
                if stock.stock > 0:
                    messages.append(f'Attention, stock {ref.name} < 2')
                    stock.stock -= 1
                    stock.save()
                else:
                    messages.append(f"Il n'y a plus de stock {ref.name}")
            stock.stock -= 1
            stock.save()

        if not messages:
            return Response(serializer.data)

        return Response(data=(serializer.data, messages))
