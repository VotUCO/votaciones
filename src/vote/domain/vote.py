from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Vote:
    id: UUID
    datetime: datetime 
    voting_id: UUID
    user_id: UUID
    vote: dict
    voted: bool



