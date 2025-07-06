from abc import ABC, abstractmethod
from typing import Optional, List

from ranked_choice.core.domain.items.ballot_item import BallotItem


class BallotRepositoryInterface(ABC):
    """
    Abstract base class for ballot repository.
    Defines the interface for ballot operations.
    """

    @abstractmethod
    def create_ballot(self, title: str, choices: List[dict], description: Optional[str] = None) -> str:
        """
        Create a new ballot with the given title, choices, and optional description.

        Args:
            title: The title of the ballot
            choices: List of choices, each with a name and description
            description: Optional description for the ballot

        Returns:
            str: The slug of the created ballot
        """
        pass

    @abstractmethod
    def get_ballot_by_slug(self, slug: str) -> Optional[BallotItem]:
        """
        Get a ballot by its slug.

        Args:
            slug: The slug of the ballot to retrieve

        Returns:
            The BallotItem object if found, None otherwise
        """
        pass

    @abstractmethod
    def list_ballots(self) -> List[BallotItem]:
        """
        List all ballots.

        Returns:
            A list of all BallotItem objects
        """
        pass
