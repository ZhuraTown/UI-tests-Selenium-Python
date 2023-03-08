from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """
    Схема пользователя
    """
    first_name: str
    last_name: str
    middle_name: str
    password: Optional[str]
    email: Optional[str]

