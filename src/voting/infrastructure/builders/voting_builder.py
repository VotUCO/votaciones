from datetime import datetime
from typing import Dict
import uuid
from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.builder import Builder
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum
from src.voting.domain.voting import Voting


class VotingBuilder(Builder):
    def build(self, json: Dict) -> Voting:
        return Voting(
            id=json.get("id") if json.get("id") else uuid.uuid4(),
            name=json.get("name"),
            state=StatusEnum(json.get("state")) if json.get("state") else None,
            winners=int(json.get("winners")) if json.get("winners") else None,
            voting_system=(
                VotingSystemEnum(json.get("voting_system"))
                if json.get("voting_system")
                else None
            ),
            privacy="True" if json.get("privacy") == 'true' else 'False',
            start_date=(
                datetime.strptime(json.get("start_date"), "%d/%m/%Y, %H:%M:%S")
                if type(json.get("start_date")) == str
                else json.get("start_date")
            ),
            end_date=(
                datetime.strptime(json.get("end_date"), "%d/%m/%Y, %H:%M:%S")
                if type(json.get("end_date")) == str
                else json.get("start_date")
            ),
            voting_creator=(
                uuid.UUID(json.get("voting_creator"))
                if json.get("voting_creator")
                else None
            ),
            created_at=datetime.now(),
            authorized_user=(
                eval(json.get("authorized_user")) if json.get("authorized_user") else []
            ),
            options=eval(json.get("options")) if json.get("options") else [],
        )

    def build_new_one(self, old_vote: Voting, new_vote: Voting) -> Voting:
        return Voting(
            id=old_vote.id,
            name=new_vote.name,
            state=StatusEnum(new_vote.state),
            winners=(
                int(new_vote.winners)
                if new_vote.winners
                else old_vote.winners
            ),
            voting_system=VotingSystemEnum(new_vote.voting_system),
            privacy=True if new_vote.privacy == "true" else "false",
            start_date=new_vote.start_date,
            end_date=new_vote.end_date,
            voting_creator=old_vote.voting_creator,
            created_at=old_vote.created_at,
            authorized_user=list(new_vote.authorized_user) if new_vote.authorized_user else None,
            options=list(new_vote.options) if new_vote.options else None,
        )
    
    def build_from_record(self, record) -> Voting:
        return Voting(
            id=record.id,
            name=record.name,
            state=record.state,
            winners=record.winners,
            voting_system=record.voting_system,
            privacy=record.privacy,
            start_date=record.start_date,
            end_date=record.end_date,
            voting_creator=record.voting_creator,
            created_at=record.created_at,
            authorized_user=[],
            options=[]
        )
