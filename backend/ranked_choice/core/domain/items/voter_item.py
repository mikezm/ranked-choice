from dataclasses import dataclass


@dataclass
class VoteItem:
    """
    Domain item representing a vote
    """
    rank: int
    choice_id: int


@dataclass
class VoterItem:
    """
    Domain item representing a voter
    """
    name: str
    ballot_id: int
    votes: list[VoteItem]