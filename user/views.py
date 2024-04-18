from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer


class CreateUserAPIView(CreateAPIView):
    serializer_class = UserSerializer
