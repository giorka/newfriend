from dataclasses import dataclass
from random import randint
from typing import NoReturn

from . import tasks


class CodeGenerator:
    DEFAULT_LENGTH: int = 6

    @classmethod
    def generate(cls, length: int = None) -> str:
        if not length:
            length: int = cls.DEFAULT_LENGTH

        return ''.join(str(randint(a=0, b=9)) for _ in range(length))


@dataclass
class Email:
    email_address: str

    def send(self, subject: str, message: str) -> NoReturn:
        tasks.send_email_message.delay(
            email_address=self.email_address,
            subject=subject,
            message=message,

        )

    def send_registration_code(self, code: str | int) -> NoReturn:
        self.send(
            subject='Подтверждение регистрации на NewFriend',
            message=('Ваш код подтверждения: <span style="color: #a86032;">' + code.__str__() + '</p>')
        )
