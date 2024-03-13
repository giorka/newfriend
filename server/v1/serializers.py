from datetime import datetime, timedelta
from typing import NoReturn, Optional

from django.contrib.auth.models import User
from django.core import validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import db
from . import utils


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields: tuple = (
            'username',
            # 'date_joined',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields: tuple = (
            'username',
            'email',
            'password',

        )
        expire_time: timedelta = timedelta(seconds=(60 * 2))

    def create(self, validated_data: dict) -> dict:
        """
        TODO: добавлять код в базу данных и рассылать его
        """

        email: utils.Email = utils.Email(email_address=validated_data['email'])
        code: str = utils.CodeGenerator.generate()
        email.send_registration_code(code=code)

        db.registration_queue.insert_one(
            document=(
                    validated_data
                    | dict(expirationTime=(datetime.utcnow() + self.Meta.expire_time))
                    | dict(secret=code)
            )
        )

        return validated_data

    def credentials_exists(self, credentials: dict) -> bool:
        return (
                not not db.registration_queue.find_one(credentials)
                or self.Meta.model.objects.filter(username=credentials.get('username')).exists()
                or self.Meta.model.objects.filter(email=credentials.get('email')).exists()
        )

    def validate(self, attrs: dict) -> dict:
        if self.credentials_exists(
                credentials=dict(
                    username=attrs.get('username'),
                    email=attrs.get('email'),
                )
        ):
            raise ValidationError('A user with that credentials already exists.')

        return super().validate(attrs)


class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    secret = serializers.CharField(
        max_length=6,
        validators=(
            validators.MinLengthValidator(6),
        ),

    )

    class Meta:
        model: User = User

    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._record: Optional[dict] = None

    def validate(self, attrs: dict) -> dict:
        record = db.registration_queue.find_one_and_delete(
            dict(
                email=attrs['email']
            )
        )

        if not record or attrs['secret'] != record['secret']:
            raise ValidationError('The code is expired.')

        self._record = record

        return super().validate(attrs=attrs)

    def save(self, **kwargs):
        return self.Meta.model.objects.create_user(
            username=self._record['username'],
            email=self._record['email'],
            password=self._record['password'],
        )
