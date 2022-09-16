from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from bar.views import RegisterView, BarViewSet, StockViewSet, StockDetailViewSet, ReferenceViewSet, RankingViewSet, \
    MenuViewSet

router = routers.SimpleRouter()
router.register('bars', BarViewSet, basename='bars')
router.register('references', ReferenceViewSet, basename='references')
router.register('menu', MenuViewSet, basename='menu')

bars_router = routers.NestedSimpleRouter(router, 'bars', lookup='bar')
bars_router.register('ranking', RankingViewSet, basename='ranking')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/-auth', include('rest_framework.urls')),
    path('api/signup/', RegisterView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('api/stock/', StockViewSet.as_view({'get': 'list', 'post': 'create'}), name='stock'),
    path('api/stock/<pk>/', StockDetailViewSet.as_view({'get': 'list'}), name='stock_detail')
]
