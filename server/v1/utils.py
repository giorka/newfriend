from typing import NoReturn, Optional


class Email:
    def __init__(self, email_address: str) -> NoReturn:
        self._email_address: str = email_address
        self._code: Optional[str] = None
