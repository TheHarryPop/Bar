from django.contrib import admin
from django.urls import path, include

from bar.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/-auth', include('rest_framework.urls')),
    path('api/signup/', RegisterView.as_view(), name='auth_signup')
]