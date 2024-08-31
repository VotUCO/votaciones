from typing import Any, Dict, List
from src.voting.domain.serializer import Serializer
from src.voting.domain.value_objects.options import Options


class OptionSerializer(Serializer):
    def serialize(self, option: Options) -> Any:
        return option

    def serialize_all(self, items: List[Any]) -> List[Dict]:
        serialized = []
        for item in items:
            serialized.append(self.serialize(item))
        return dict(options=serialized)
