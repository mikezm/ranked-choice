from abc import ABC, abstractmethod
from typing import Optional, List

from ranked_choice.core.models import Ballot


class BallotRepositoryInterface(ABC):
    """
    Abstract base class for ballot repository.
    Defines the interface for ballot operations.
    """

    @abstractmethod
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