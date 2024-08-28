from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from uuid import UUID
from src.voting.domain.value_objects.status_enum import StatusEnum
from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum


@dataclass
class Voting:
    id: UUID
    name: str
    state: StatusEnum
    winners: int
    voting_system: VotingSystemEnum
    privacy: str
    start_date: datetime
    end_date: datetime
    voting_creator: str
    created_at: datetime
    options: list
    authorized_user: Optional[list]

    def is_voting_active(self) -> bool:
        return datetime.now() > self.start_date and datetime.now() < self.end_date

    def is_public(self) -> bool:
        return self.privacy == "False"

    def is_published(self) -> bool:
        return self.state == StatusEnum.PUBLISHED.value

    def is_draft(self) -> bool:
        return self.state == StatusEnum.DRAFT.value

    def add_option(self, option) -> None:
        self.options.append(option)
