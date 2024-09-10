from typing import Dict
from src.vote.domain.builder import Builder
from src.vote.domain.vote import Vote
from uuid import uuid4
from datetime import datetime

class VoteBuilder(Builder):
    def build(self, json: Dict) -> Vote:
        return Vote(
            id=uuid4() if json.get("id") == None else json.get("id"),
            datetime=datetime.now() if json.get("datetime") == None else json.get("datetime"),
            voting_id=json.get("voting_id"),
            user_id=json.get("user_id"),
            vote=json.get("vote"),
            voted= True if json.get("vote") == "True" else False
        )
    
    def build_from_record(self, record) -> Vote:
        return Vote(
            id=record.votetoken,
            datetime=record.votedatetime,
            voting_id=record.votingid,
            user_id=record.userid,
            vote=None,
            voted=None,
        )