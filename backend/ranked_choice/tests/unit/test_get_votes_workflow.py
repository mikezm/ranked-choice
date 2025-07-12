import unittest
from unittest.mock import Mock

from faker import Faker

from ranked_choice.core.domain.items.ballot_item import (
    BallotItem,
    BallotResultItem,
    ChoiceItem,
)
from ranked_choice.core.domain.items.voter_item import VoteItem, VoterItem
from ranked_choice.core.domain.workflows.get_votes_workflow import get_votes_workflow
from ranked_choice.core.repositories.ballot_repository_interface import (
    BallotRepositoryInterface,
)


class TestGetVotesWorkflow(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.mock_repository = Mock(spec=BallotRepositoryInterface)

    def test_simple_majority(self):
        slug = self.fake.slug()
        choice_id1 = 1
        choice_id2 = 2
        choice_id3 = 3
        ballot_id = self.fake.pyint()
        ballot_item = BallotItem(
            id=ballot_id,
            title=self.fake.sentence(nb_words=3),
            slug=slug,
            description=self.fake.sentence(),
            choices=[
                ChoiceItem(
                    id=choice_id1, name="Choice 1",
                    description=self.fake.sentence()
                ),
                ChoiceItem(
                    id=choice_id2, name="Choice 2",
                    description=self.fake.sentence()
                ),
                ChoiceItem(
                    id=choice_id3, name="Choice 3",
                    description=self.fake.sentence()
                ),
            ]
        )

        voter_items = [
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id1),
                VoteItem(rank=2, choice_id=choice_id2),
                VoteItem(rank=3, choice_id=choice_id3),
            ]),
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id1),
                VoteItem(rank=2, choice_id=choice_id3),
                VoteItem(rank=3, choice_id=choice_id2),
            ]),
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id2),
                VoteItem(rank=2, choice_id=choice_id1),
                VoteItem(rank=3, choice_id=choice_id3),
            ]),
        ]

        self.mock_repository.get_ballot_by_slug.return_value = ballot_item
        self.mock_repository.get_votes_by_ballot_id.return_value = voter_items

        result = get_votes_workflow(slug, self.mock_repository)

        self.mock_repository.get_ballot_by_slug.assert_called_once_with(slug=slug)
        self.mock_repository.get_votes_by_ballot_id.assert_called_once_with(ballot_id=ballot_item.id)

        self.assertIsInstance(result, BallotResultItem)
        self.assertEqual(result.winner_id, choice_id1)
        self.assertEqual(result.winner_name, "Choice 1")
        self.assertEqual(len(result.rounds), 1)
        self.assertEqual(result.rounds[0][choice_id1], 2)
        self.assertEqual(result.rounds[0][choice_id2], 1)

    def test_no_simple_majority(self):
        slug = self.fake.slug()
        choice_id1 = 1
        choice_id2 = 2
        choice_id3 = 3
        ballot_id = self.fake.pyint()
        ballot_item = BallotItem(
            id=ballot_id,
            title=self.fake.sentence(nb_words=3),
            slug=slug,
            description=self.fake.sentence(),
            choices=[
                ChoiceItem(
                    id=choice_id1, name="Choice 1",
                    description=self.fake.sentence()
                ),
                ChoiceItem(
                    id=choice_id2, name="Choice 2",
                    description=self.fake.sentence()
                ),
                ChoiceItem(
                    id=choice_id3, name="Choice 3",
                    description=self.fake.sentence()
                ),
            ]
        )

        voter_items = [
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id1),
                VoteItem(rank=2, choice_id=choice_id2),
                VoteItem(rank=3, choice_id=choice_id3),
            ]),
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id2),
                VoteItem(rank=2, choice_id=choice_id1),
                VoteItem(rank=3, choice_id=choice_id3),
            ]),
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id3),
                VoteItem(rank=2, choice_id=choice_id1),
                VoteItem(rank=3, choice_id=choice_id2),
            ]),
        ]

        self.mock_repository.get_ballot_by_slug.return_value = ballot_item
        self.mock_repository.get_votes_by_ballot_id.return_value = voter_items

        result = get_votes_workflow(slug, self.mock_repository)

        self.mock_repository.get_ballot_by_slug.assert_called_once_with(slug=slug)
        self.mock_repository.get_votes_by_ballot_id.assert_called_once_with(ballot_id=ballot_item.id)

        self.assertIsInstance(result, BallotResultItem)
        self.assertEqual(len(result.rounds), 2)
        self.assertEqual(result.rounds[0][choice_id1], 1)
        self.assertEqual(result.rounds[0][choice_id2], 1)
        self.assertEqual(result.rounds[0][choice_id3], 1)

        has_expected_choices = (
            (choice_id1 in result.rounds[1] and choice_id2 in result.rounds[1]) or
            (choice_id2 in result.rounds[1] and choice_id3 in result.rounds[1])
        )
        self.assertTrue(has_expected_choices)
        self.assertEqual(sum(result.rounds[1].values()), 3)

    def test_tie_scenario(self):
        slug = self.fake.slug()
        choice_id1 = 1
        choice_id2 = 2
        ballot_id = self.fake.pyint()
        ballot_item = BallotItem(
            id=ballot_id,
            title=self.fake.sentence(nb_words=3),
            slug=slug,
            description=self.fake.sentence(),
            choices=[
                ChoiceItem(
                    id=choice_id1, name="Choice 1",
                    description=self.fake.sentence()
                ),
                ChoiceItem(
                    id=choice_id2, name="Choice 2",
                    description=self.fake.sentence()
                ),
            ]
        )

        voter_items = [
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id1),
            ]),
            VoterItem(name=self.fake.name(), ballot_id=ballot_id, votes=[
                VoteItem(rank=1, choice_id=choice_id2),
            ]),
        ]

        self.mock_repository.get_ballot_by_slug.return_value = ballot_item
        self.mock_repository.get_votes_by_ballot_id.return_value = voter_items

        result = get_votes_workflow(slug, self.mock_repository)

        self.mock_repository.get_ballot_by_slug.assert_called_once_with(slug=slug)
        self.mock_repository.get_votes_by_ballot_id.assert_called_once_with(ballot_id=ballot_item.id)

        self.assertIsInstance(result, BallotResultItem)
        self.assertEqual(len(result.rounds), 1)
        self.assertEqual(result.rounds[0][choice_id1], 1)
        self.assertEqual(result.rounds[0][choice_id2], 1)

        self.assertTrue(result.winner_id in [choice_id1, choice_id2])

    def test_no_votes(self):
        slug = self.fake.slug()
        choice_id1 = 1
        choice_id2 = 2
        ballot_id = self.fake.pyint()
        ballot_item = BallotItem(
            id=ballot_id,
            title=self.fake.sentence(nb_words=3),
            slug=slug,
            description=self.fake.sentence(),
            choices=[
                ChoiceItem(
                    id=choice_id1, name="Choice 1",
                    description=self.fake.sentence()
                ),
                ChoiceItem(
                    id=choice_id2, name="Choice 2",
                    description=self.fake.sentence()
                ),
            ]
        )

        voter_items = []

        self.mock_repository.get_ballot_by_slug.return_value = ballot_item
        self.mock_repository.get_votes_by_ballot_id.return_value = voter_items

        result = get_votes_workflow(slug, self.mock_repository)

        self.mock_repository.get_ballot_by_slug.assert_called_once_with(slug=slug)
        self.mock_repository.get_votes_by_ballot_id.assert_called_once_with(ballot_id=ballot_item.id)

        self.assertIsInstance(result, BallotResultItem)
        self.assertEqual(result.winner_id, -1)
        self.assertEqual(result.winner_name, "No votes found")
        self.assertEqual(result.rounds, [])

    def test_get_votes_for_nonexistent_ballot(self):
        slug = self.fake.slug()
        self.mock_repository.get_ballot_by_slug.return_value = None

        result = get_votes_workflow(slug, self.mock_repository)
        self.mock_repository.get_ballot_by_slug.assert_called_once_with(slug=slug)
        self.mock_repository.get_votes_by_ballot_id.assert_not_called()

        self.assertIsInstance(result, BallotResultItem)
        self.assertEqual(result.winner_id, -1)
        self.assertEqual(result.winner_name, "No ballot found")
        self.assertEqual(result.rounds, [])
