from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ChoiceItem:
    """
    Domain item representing a ballot choice.
    """
    id: int
    name: str
    description: Optional[str] = None


@dataclass
class BallotItem:
    """
    Domain item representing a ballot.
    """
    id: int
    title: str
    slug: str
    description: Optional[str] = None
    choices: List[ChoiceItem] = None

    def __post_init__(self):
        if self.choices is None:
            self.choices = []
