from abc import ABC, abstractmethod
from typing import Optional, List
from django.utils.text import slugify

from ranked_choice.core.models import Ballot, Choice


class BallotRepositoryInterface(ABC):
    """
    Abstract base class for ballot repository.
    Defines the interface for ballot operations.
    """

    @abstractmethod
    def create_ballot(self, title: str, description: Optional[str] = None) -> Ballot:
        """
        Create a new ballot with the given title and optional description.

        Args:
            title: The title of the ballot
            description: Optional description for the ballot

        Returns:
            The created Ballot object
        """
        pass

    @abstractmethod
    def get_ballot_by_id(self, ballot_id: int) -> Optional[Ballot]:
        """
        Get a ballot by its ID.

        Args:
            ballot_id: The ID of the ballot to retrieve

        Returns:
            The Ballot object if found, None otherwise
        """
        pass

    @abstractmethod
    def get_ballot_by_slug(self, slug: str) -> Optional[Ballot]:
        """
        Get a ballot by its slug.

        Args:
            slug: The slug of the ballot to retrieve

        Returns:
            The Ballot object if found, None otherwise
        """
        pass

    @abstractmethod
    def list_ballots(self) -> List[Ballot]:
        """
        List all ballots.

        Returns:
            A list of all Ballot objects
        """
        pass


class BallotRepository(BallotRepositoryInterface):
    """
    Django implementation of the ballot repository.
    Uses Django models to interact with the database.
    """

    def create_ballot(self, title: str, description: Optional[str] = None) -> Ballot:
        """
        Create a new ballot with the given title and optional description.

        Args:
            title: The title of the ballot
            description: Optional description for the ballot

        Returns:
            The created Ballot object
        """
        # Generate a slug from the title
        slug = slugify(title)

        # Create the ballot
        ballot = Ballot.objects.create(
            title=title,
            slug=slug
        )

        # If description is provided, create a choice with it
        if description:
            Choice.objects.create(
                ballot=ballot,
                name="Description",
                description=description
            )

        return ballot

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
