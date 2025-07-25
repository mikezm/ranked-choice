from typing import List, Optional

from ranked_choice.core.repositories.ballot_repository import (
    BallotRepository,
    BallotRepositoryInterface,
)


def create_ballot_workflow(
    title: str,
    choices: List[dict],
    description: Optional[str] = None,
    ballot_repository: Optional[BallotRepositoryInterface] = None
) -> str:
    """
    Workflow to create a new ballot.

    Args:
        title: The title of the ballot
        choices: Required list of choices, each with a name and description
        description: Optional description for the ballot
        ballot_repository: Optional repository instance for testing purposes

    Returns:
        str: The slug of the created ballot

    Raises:
        ValueError: If the title is empty or choices is empty
    """
    # Validate inputs
    if not title:
        raise ValueError("Ballot title cannot be empty")

    if not choices:
        raise ValueError("Choices cannot be empty")

    repository = ballot_repository or BallotRepository()

    return repository.create_ballot(title, choices, description)
