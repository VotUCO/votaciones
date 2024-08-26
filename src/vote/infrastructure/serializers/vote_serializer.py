from typing import Dict
from src.vote.domain.serializer import Serializer
from src.vote.domain.vote import Vote


class VoteSerializer(Serializer):
    def serialize(self, vote: Vote) -> Dict:
        return dict(
            id=vote.id,
            datetime=vote.datetime,
            voting_id=vote.voting_id,
        )