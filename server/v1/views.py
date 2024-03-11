from rest_framework.generics import CreateAPIView

from . import serializers


class RegisterAPIView(CreateAPIView):
    serializer_class = serializers.RegisterUserSerializer


class VerifyAPIView(CreateAPIView):
    serializer_class = serializers.VerifyUserSerializer
