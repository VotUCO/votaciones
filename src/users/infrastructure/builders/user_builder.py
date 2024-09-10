from typing import Any, Dict
from src.users.domain.builder import Builder
from src.users.domain.user import User
from src.users.domain.value_objects.gender_enum import GenderEnum
from src.users.domain.value_objects.rol_enum import RolEnum
import uuid
from datetime import datetime
import hashlib


class UserBuilder(Builder):
    def __init__(self):
        self.__hasher_password = hashlib.sha256()

    def build(self, json: Dict) -> Any:
        password = str(json.get("password")).encode()
        password = self.__hasher_password.update(password)
        return User(
            id=uuid.uuid4() if json.get("id") == None else json.get("id"),
            name=json.get("name"),
            surname=json.get("surname"),
            email=json.get("email"),
            password=self.__hasher_password.hexdigest(),
            gender=GenderEnum(json.get("gender")) if json.get("gender") else None,
            birthDate=
                datetime.strptime(json.get("birthDate"), "%d-%m-%Y")
                if json.get("birthDate")
                else None
            ,
            rol=RolEnum(RolEnum.USER) if json.get("rol") == None else RolEnum(RolEnum.ADMIN) if json.get("rol") == "admin" else RolEnum(RolEnum.USER),
        )

    def build_from_record(self, record: Any) -> Any:
        return User(
            id=record.id,
            name=record.name,
            surname=record.surname,
            email=record.email,
            password=record.password,
            gender=GenderEnum(record.gender),
            birthDate=record.birth_date,
            rol=RolEnum(record.rol),
        )
    
    def build_from_record_admin(self, record: Any) -> Any:
        return User(
            id=record.id,
            name=record.name,
            surname=record.surname,
            email=record.email,
            password=None,
            gender=GenderEnum(record.gender),
            birthDate=record.birth_date,
            rol=RolEnum(record.rol),
        )
    
    def build_from_record_vote(self, record: Any) -> Any:
        return User(
            id=record.id,
            name=record.name,
            surname=record.surname,
            email=record.email,
            password=None,
            gender=GenderEnum(record.gender),
            birthDate=record.birth_date,
            rol=None,
        )

    def build_from_record_email_pass(self, record: Any) -> Any:
        return User(
            id=None,
            name=None,
            surname=None,
            email=record.email,
            password=record.password,
            gender=None,
            birthDate=None,
            rol=None,
        )
