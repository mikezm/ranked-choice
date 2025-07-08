import uuid
from typing import List, Optional

from django.utils.text import slugify

from ranked_choice.core.domain.items.ballot_item import BallotItem, ChoiceItem
from ranked_choice.core.domain.items.voter_item import VoteItem, VoterItem
from ranked_choice.core.models import Ballot, Choice, Vote, Voter
from ranked_choice.core.repositories.ballot_repository_interface import (
    BallotRepositoryInterface,
)


def build_choices(ballot) -> List[ChoiceItem]:
    choices = Choice.objects.filter(ballot=ballot)
    choice_items = []
    for choice in choices:
        choice_items.append(ChoiceItem(
            id=choice.id,
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
                id=ballot.id,
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
                id=ballot.id,
                title=ballot.title,
                slug=ballot.slug,
                description=ballot.description,
                choices=choice_items
            ))

        return ballot_items

    def create_voter(
            self,
            name: str,
            ballot_id: int,
            votes: List[dict]
    ) -> None:
        voter = Voter.objects.create(
            name=name,
            ballot_id=ballot_id,
        )
        for vote in votes:
            Vote.objects.create(
                voter=voter,
                rank=vote['rank'],
                choice_id=vote['choice_id']
            )


    def get_votes_by_ballot_id(self, ballot_id: int) -> List[VoterItem]:
        voter_items = []
        voters = Voter.objects.filter(ballot_id=ballot_id)
        for voter in voters:
            votes = Vote.objects.filter(voter_id=voter.id)
            vote_items = []
            for vote in votes:
                vote_items.append(VoteItem(
                    rank=vote.rank,
                    choice_id=vote.choice_id
                ))

            voter_items.append(VoterItem(
                name=voter.name,
                ballot_id=ballot_id,
                votes=vote_items
            ))

        return voter_items

