from dataclasses import dataclass
from uuid import UUID


@dataclass
class Options:
    voting_id: UUID
    option_name: str
