import uuid
from typing import List, Optional

from django.utils.text import slugify

from ranked_choice.core.domain.items.ballot_item import BallotItem, ChoiceItem
from ranked_choice.core.models import Ballot, Choice
from ranked_choice.core.repositories.ballot_repository_interface import (
    BallotRepositoryInterface,
)


def build_choices(ballot) -> List[ChoiceItem]:
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

    def create_ballot(
            self,
            title: str,
            choices: List[dict],
            description: Optional[str] = None
    ) -> str:
        """
        Create a new ballot with the given title, choices, and optional description.

        Args:
            title: The title of the ballot
            choices: List of choices, each with a name and description
            description: Optional description for the ballot

        Returns:
            str: The slug of the created ballot
        """
        unique_id = str(uuid.uuid4())[:8]
        slug = f'{slugify(title)}-{unique_id}'

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

        return slug

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
            choice_items = build_choices(ballot)

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
            choice_items = build_choices(ballot)
            ballot_items.append(BallotItem(
                title=ballot.title,
                slug=ballot.slug,
                description=ballot.description,
                choices=choice_items
            ))

        return ballot_items
