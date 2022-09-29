from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from bar.views import RegisterView, BarViewSet, StockViewSet, ReferenceViewSet, RankingViewSet, MenuViewSet, \
    OrderViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/-auth', include('rest_framework.urls')),
    path('api/signup/', RegisterView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/bars/', BarViewSet.as_view({'get': 'list', 'post': 'create'}), name='Bars'),
    path('api/bar/<int:pk>/', BarViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='Bar Details'),
    path('api/references/', ReferenceViewSet.as_view({'get': 'list', 'post': 'create'}), name='References'),
    path('api/references/<int:pk>/', ReferenceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete':
         'destroy'}), name='Reference Details'),
    path('api/stock/<int:pk>/', StockViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update',
                                                      'delete': 'destroy'}), name='Stock Details'),
    path('api/menu/', MenuViewSet.as_view({'get': 'list'}, name='Menu')),
    # path('api/menu/<int: pk>/', MenuViewSet.as_view({'get': 'retrieve'}, name='Bar Menu')),
    path('api/orders/', OrderViewSet.as_view({'get': 'list'}), name='Orders'),
    path('api/order/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='Order Details'),
    path('api/bars/ranking/', RankingViewSet.as_view(), name='Ranking'),
    path('api/orders/bars/ranking/', RankingViewSet.as_view(), name='Ranking'),
]
