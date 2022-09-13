from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
