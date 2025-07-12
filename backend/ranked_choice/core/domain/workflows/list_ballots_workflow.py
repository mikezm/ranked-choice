from typing import List, Optional

from ranked_choice.core.domain.items.ballot_item import BallotItem
from ranked_choice.core.repositories.ballot_repository import (
    BallotRepository,
    BallotRepositoryInterface,
)


def list_ballots_workflow(
    ballot_repository: Optional[BallotRepositoryInterface] = None
) -> List[BallotItem]:
    """
    Workflow to list all ballots.

    Args:
        ballot_repository: Optional repository instance for dependency injection

    Returns:
        List[BallotItem]: A list of all ballot items
    """
    repository = ballot_repository or BallotRepository()

    return repository.list_ballots()