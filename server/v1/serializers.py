from django.contrib.auth.models import User
from django.core import validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import db


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',

        )

    def create(self, validated_data: dict) -> dict:
        db.registration_queue.insert_one(document=validated_data)

        return validated_data

    @staticmethod
    def credentials_exists(credentials: dict) -> bool:
        return not not db.registration_queue.find_one(credentials)

    def validate(self, data: dict) -> dict:
        if self.credentials_exists(
                credentials=dict(
                    username=data.get('username'),
                    email=data.get('email'),
                )
        ):
            raise ValidationError('A user with that credentials already exists.')

        return super().validate(data)


class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    secret = serializers.CharField(
        max_length=6,
        validators=(
            validators.MinLengthValidator(6),
        ),

    )

    class Meta:
        model = User

    def create(self, validated_data: dict) -> dict:
        ...
