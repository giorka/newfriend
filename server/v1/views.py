from typing import NoReturn

from django.contrib.auth import login, logout
from rest_framework import views
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import serializers


class RegisterAPIView(CreateAPIView):
    serializer_class = serializers.RegisterUserSerializer


class VerifyAPIView(views.APIView):
    serializer_class = serializers.VerifyUserSerializer
    model = serializer_class.Meta.model

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(
            request=request,
            user=user,
        )

        return Response(
            data=serializers.UserSerializer(user).data
        )


class LogoutAPIView(views.APIView):
    @staticmethod
    def post(request) -> NoReturn:
        logout(request=request)

        return Response(status=200)
