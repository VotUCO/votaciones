from dataclasses import dataclass
from uuid import UUID


@dataclass
class AuthorizedUser:
    voting_id: UUID
    user_id: UUID
