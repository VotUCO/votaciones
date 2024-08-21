from dataclasses import dataclass
from uuid import UUID
import datetime

from src.users.domain.value_objects.email import Email
from src.users.domain.value_objects.gender_enum import GenderEnum
from src.users.domain.value_objects.rol_enum import RolEnum


@dataclass
class User:
    id: UUID
    name: str
    surname: str
    email: Email
    password: str
    gender: GenderEnum
    birthDate: datetime
    rol: RolEnum
