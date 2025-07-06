from typing import Optional, List
from django.utils.text import slugify
from ranked_choice.core.repositories.ballot_repository_interface import BallotRepositoryInterface
from ranked_choice.core.models import Ballot, Choice
from ranked_choice.core.domain.items.ballot_item import BallotItem, ChoiceItem


def build_choices(ballot):
    choices = Choice.objects.filter(ballot=ballot)
    choice_items = []
    for choice in choices:
        choice_items.append(ChoiceItem(
            name=choice.name,
            description=choice.description
        ))

    return choice_items


class BallotRepository(BallotRepositoryInterface):
    """
    Django implementation of the ballot repository.
    Uses Django models to interact with the database.
    """

    def create_ballot(self, title: str, choices: List[dict], description: Optional[str] = None) -> None:
        """
        Create a new ballot with the given title, choices, and optional description.

        Args:
            title: The title of the ballot
            choices: List of choices, each with a name and description
            description: Optional description for the ballot

        Returns:
            None
        """
        # Generate a slug from the title
        slug = slugify(title)

        # Create the ballot
        ballot = Ballot.objects.create(
            title=title,
            slug=slug,
            description=description
        )

        # Create the choices
        for choice in choices:
            Choice.objects.create(
                ballot=ballot,
                name=choice['name'],
                description=choice.get('description', '')
            )

        # No return value

    def get_ballot_by_slug(self, slug: str) -> Optional[BallotItem]:
        """
        Get a ballot by its slug.

        Args:
            slug: The slug of the ballot to retrieve

        Returns:
            The BallotItem object if found, None otherwise
        """
        try:
            ballot = Ballot.objects.get(slug=slug)

            # Get all choices for this ballot
            choice_items = build_choices(ballot)

            # Create and return the BallotItem
            return BallotItem(
                title=ballot.title,
                slug=ballot.slug,
                description=ballot.description,
                choices=choice_items
            )
        except Ballot.DoesNotExist:
            return None

    def list_ballots(self) -> List[BallotItem]:
        """
        List all ballots.

        Returns:
            A list of all BallotItem objects
        """
        ballots = Ballot.objects.all()
        ballot_items = []

        for ballot in ballots:
            # Get all choices for this ballot
            choice_items = build_choices(ballot)

            # Create and append the BallotItem
            ballot_items.append(BallotItem(
                title=ballot.title,
                slug=ballot.slug,
                description=ballot.description,
                choices=choice_items
            ))

        return ballot_items
