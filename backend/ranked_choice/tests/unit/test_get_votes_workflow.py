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

        # Group round items by round_index
        round_items_by_round = {}
        for item in result.rounds:
            if item.round_index not in round_items_by_round:
                round_items_by_round[item.round_index] = []
            round_items_by_round[item.round_index].append(item)

        # Check first round
        first_round = round_items_by_round.get(0, [])
        self.assertEqual(len(first_round), 2)  # Two choices received votes

        # Find the RoundItem for Choice 1 and verify it has 2 votes
        choice1_item = next(
            (item for item in first_round if item.name == "Choice 1"), None
        )
        self.assertIsNotNone(choice1_item)
        self.assertEqual(choice1_item.votes, 2)

        # Find the RoundItem for Choice 2 and verify it has 1 vote
        choice2_item = next(
            (item for item in first_round if item.name == "Choice 2"), None
        )
        self.assertIsNotNone(choice2_item)
        self.assertEqual(choice2_item.votes, 1)

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

        # Group round items by round_index
        round_items_by_round = {}
        for item in result.rounds:
            if item.round_index not in round_items_by_round:
                round_items_by_round[item.round_index] = []
            round_items_by_round[item.round_index].append(item)

        # Check first round
        first_round = round_items_by_round.get(0, [])
        self.assertEqual(len(first_round), 3)

        choice1_item = next(
            (item for item in first_round if item.name == "Choice 1"), None
        )
        self.assertIsNotNone(choice1_item)
        self.assertEqual(choice1_item.votes, 1)

        choice2_item = next(
            (item for item in first_round if item.name == "Choice 2"), None
        )
        self.assertIsNotNone(choice2_item)
        self.assertEqual(choice2_item.votes, 1)

        choice3_item = next(
            (item for item in first_round if item.name == "Choice 3"), None
        )
        self.assertIsNotNone(choice3_item)
        self.assertEqual(choice3_item.votes, 1)

        # Check second round
        second_round = round_items_by_round.get(1, [])
        self.assertGreaterEqual(len(second_round), 2)

        # Check that the total votes in the second round is 3
        total_votes_second_round = sum(item.votes for item in second_round)
        self.assertEqual(total_votes_second_round, 3)

        # Check that the second round has the expected choices
        second_round_names = [item.name for item in second_round]
        has_expected_choices = (
            ("Choice 1" in second_round_names and "Choice 2" in second_round_names) or
            ("Choice 2" in second_round_names and "Choice 3" in second_round_names)
        )
        self.assertTrue(has_expected_choices)

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

        # Group round items by round_index
        round_items_by_round = {}
        for item in result.rounds:
            if item.round_index not in round_items_by_round:
                round_items_by_round[item.round_index] = []
            round_items_by_round[item.round_index].append(item)

        # Check first round
        first_round = round_items_by_round.get(0, [])
        self.assertEqual(len(first_round), 2)  # Two choices received votes

        # Find the RoundItem for Choice 1 and verify it has 1 vote
        choice1_item = next(
            (item for item in first_round if item.name == "Choice 1"), None
        )
        self.assertIsNotNone(choice1_item)
        self.assertEqual(choice1_item.votes, 1)

        # Find the RoundItem for Choice 2 and verify it has 1 vote
        choice2_item = next(
            (item for item in first_round if item.name == "Choice 2"), None
        )
        self.assertIsNotNone(choice2_item)
        self.assertEqual(choice2_item.votes, 1)

        # Check that the winner is one of the two choices
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
