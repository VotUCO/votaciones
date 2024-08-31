from typing import Any, Dict, List
from src.voting.domain.serializer import Serializer
from src.voting.domain.voting import Voting


class VotingSerializer(Serializer):
    def serialize(self, voting: Voting) -> Dict:
        return dict(
            id=voting.id,
            name=voting.name,
            state=voting.state.value,
            voting_system=voting.voting_system.value,
            privacy=voting.privacy,
            start_date=voting.start_date,
            end_date=voting.end_date,
            voting_creator=voting.voting_creator,
            created_at=voting.created_at,
        )

    def for_user_serializer(self, voting: Voting) -> Dict:
        return dict(
            id=voting.id,
            name=voting.name,
            winners=voting.winners,
            voting_system=voting.voting_system.value,
            start_date=voting.start_date,
            end_date=voting.end_date,
        )
    
    def for_user_serializer_modify(self, voting: Voting) -> Dict:
        return dict(
            id=voting.id,
            name=voting.name,
            winners=voting.winners,
            voting_system=voting.voting_system,
            start_date=voting.start_date,
            end_date=voting.end_date,
        )
    
    def for_user_serializer_plain(self, voting: Voting) -> Dict:
        return dict(
            id=voting.id,
            name=voting.name,
            winners=voting.winners,
            voting_system=voting.voting_system,
            start_date=voting.start_date,
            end_date=voting.end_date,
        )

    def for_user_all_serializer(self, votings: List[Voting]) -> List[Voting]:
        votings_list = []
        for vote in votings:
            votings_list.append(self.for_user_serializer(vote))
        return votings_list
    
    def for_user_all_serializer_plain(self, votings: List[Voting]) -> List[Voting]:
        votings_list = []
        for vote in votings:
            votings_list.append(self.for_user_serializer_plain(vote))
        return votings_list

    def for_user_record_serializer(self, voting: Any) -> Dict:
        return dict(
            id=voting.id,
            name=voting.name,
            winners=voting.winners,
            voting_system=voting.voting_system,
            start_date=voting.start_date,
            end_date=voting.end_date,
        )

    def for_user_record_all_serializer(self, votings: List[Voting]) -> List[Voting]:
        votings_list = []
        for vote in votings:
            votings_list.append(self.for_user_record_serializer(vote))
        return votings_list
