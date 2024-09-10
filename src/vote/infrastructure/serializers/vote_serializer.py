from typing import Dict
from src.vote.domain.serializer import Serializer
from src.vote.domain.vote import Vote
from src.voting.domain.voting import Voting
from src.users.domain.user import User


class VoteSerializer(Serializer):
    def serialize(self, vote: Vote) -> Dict:
        return dict(
            id=vote.id,
            datetime=vote.datetime,
            voting_id=vote.voting_id,
        )
    
    def serialize_checker(self, vote: Vote, voting: Voting, user: User) -> Dict:
        return dict(
            id=vote.id,
            datetime=vote.datetime,
            voting_id=vote.voting_id,
            name=voting.name,
            user=user.email,
        )