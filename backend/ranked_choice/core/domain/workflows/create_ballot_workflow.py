from typing import Optional, List

from ranked_choice.core.repositories.ballot_repository import BallotRepository


def create_ballot_workflow(
    ballot_repository: BallotRepository,
    title: str,
    description: Optional[str] = None,
    choices: Optional[List[dict]] = None
) -> str:
    """
    Workflow to create a new ballot.

    Args:
        ballot_repository: The repository to use for creating the ballot
        title: The title of the ballot
        description: Optional description for the ballot
        choices: Optional list of choices, each with a name and description

    Returns:
        str: The slug of the created ballot

    Raises:
        ValueError: If the title is empty
    """
    # Validate inputs
    if not title:
        raise ValueError("Ballot title cannot be empty")

    # Generate the slug from the title
    from django.utils.text import slugify
    slug = slugify(title)

    # Create the ballot using the repository
    ballot_repository.create_ballot(title, description, choices)

    # Return the slug
    return slug
