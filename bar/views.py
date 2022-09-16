from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

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
    queryset = Stock.objects.all()


class StockDetailViewSet(ModelViewSet):

    # permission_classes = [IsAuthenticated]
    serializer_class = StockDetailSerializer

    def get_queryset(self):
        return Stock.objects.filter(comptoir=self.kwargs['pk'])


class RankingViewSet(ModelViewSet):

    pass

    # permission_classes = []
    # serializer_class =


class MenuViewSet(ModelViewSet):

    permission_classes = []
    serializer_class = MenuListSerializer

    def get_queryset(self):
        return Reference.objects.all()
