from typing import Optional, List
from django.utils.text import slugify
from ranked_choice.core.repositories.ballot_repository_interface import BallotRepositoryInterface
from ranked_choice.core.models import Ballot, Choice



class BallotRepository(BallotRepositoryInterface):
    """
    Django implementation of the ballot repository.
    Uses Django models to interact with the database.
    """

    def create_ballot(self, title: str, description: Optional[str] = None, choices: Optional[List[dict]] = None) -> None:
        """
        Create a new ballot with the given title, optional description, and optional choices.

        Args:
            title: The title of the ballot
            description: Optional description for the ballot
            choices: Optional list of choices, each with a name and description

        Returns:
            None
        """
        # Generate a slug from the title
        slug = slugify(title)

        # Create the ballot
        ballot = Ballot.objects.create(
            title=title,
            slug=slug
        )

        # If description is provided, add it to the ballot
        if description:
            Choice.objects.create(
                ballot=ballot,
                name="Description",
                description=description
            )

        # If choices are provided, create them
        if choices:
            for choice in choices:
                Choice.objects.create(
                    ballot=ballot,
                    name=choice['name'],
                    description=choice.get('description', '')
                )

        # No return value

    def get_ballot_by_id(self, ballot_id: int) -> Optional[Ballot]:
        """
        Get a ballot by its ID.

        Args:
            ballot_id: The ID of the ballot to retrieve

        Returns:
            The Ballot object if found, None otherwise
        """
        try:
            return Ballot.objects.get(id=ballot_id)
        except Ballot.DoesNotExist:
            return None

    def get_ballot_by_slug(self, slug: str) -> Optional[Ballot]:
        """
        Get a ballot by its slug.

        Args:
            slug: The slug of the ballot to retrieve

        Returns:
            The Ballot object if found, None otherwise
        """
        try:
            return Ballot.objects.get(slug=slug)
        except Ballot.DoesNotExist:
            return None

    def list_ballots(self) -> List[Ballot]:
        """
        List all ballots.

        Returns:
            A list of all Ballot objects
        """
        return list(Ballot.objects.all())
