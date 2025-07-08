from typing import List, Optional

from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.core.repositories.ballot_repository_interface import (
    BallotRepositoryInterface,
)


def create_vote_workflow(
        name: str,
        ballot_id: int,
        votes: List[dict],
        ballot_repository: Optional[BallotRepositoryInterface] = None
) -> None:
    if len(votes) == 0:
        return

    ballot_repository = ballot_repository or BallotRepository()
    ballot_repository.create_voter(
        name=name,
        ballot_id=ballot_id,
        votes=votes
    )