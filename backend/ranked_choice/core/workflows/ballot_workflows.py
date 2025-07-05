from typing import Optional

from ranked_choice.core.models import Ballot
from ranked_choice.core.repositories.ballot_repository import BallotRepository


def create_new_ballot(
    ballot_repository: BallotRepository,
    title: str,
    description: Optional[str] = None
) -> Ballot:
    """
    Workflow to create a new ballot.

    Args:
        ballot_repository: The repository to use for creating the ballot
        title: The title of the ballot
        description: Optional description for the ballot

    Returns:
        The created Ballot object

    Raises:
        ValueError: If the title is empty
    """
    # Validate inputs
    if not title:
        raise ValueError("Ballot title cannot be empty")

    # Create the ballot using the repository
    ballot = ballot_repository.create_ballot(title, description)

    return ballot
