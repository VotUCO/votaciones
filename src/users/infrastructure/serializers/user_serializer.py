from typing import Any, Dict, List
from src.users.domain.serializer import Serializer
from src.users.domain.user import User


class UserSerializer(Serializer):
    def serialize(self, user: User) -> Dict:
        return dict(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            password=user.password,
            gender=user.gender.value,
            birthDate=user.birthDate,
            rol=user.rol.value,
        )

    def serialize_all(self, items: List[Any]) -> List[Dict]:
        serialized = []
        for item in items:
            serialized.append(self.serialize(item))
        return serialized
