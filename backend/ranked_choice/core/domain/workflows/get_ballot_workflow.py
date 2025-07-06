from typing import Optional

from ranked_choice.core.domain.items.ballot_item import BallotItem
from ranked_choice.core.repositories.ballot_repository import (
    BallotRepository,
    BallotRepositoryInterface,
)


def get_ballot_workflow(
    slug: str,
    ballot_repository: Optional[BallotRepositoryInterface] = None
) -> Optional[BallotItem]:
    """
    Workflow to create a new ballot.

    Args:
        slug: The slug of the ballot

    Returns:
        BallotItem: The ballot item with the given slug
        :param slug:
        :param ballot_repository:
    """

    repository = ballot_repository or BallotRepository()

    return repository.get_ballot_by_slug(slug=slug)
