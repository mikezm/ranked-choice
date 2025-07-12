import unittest
from unittest.mock import Mock

from faker import Faker

from ranked_choice.core.domain.items.ballot_item import BallotItem, ChoiceItem
from ranked_choice.core.domain.workflows.list_ballots_workflow import (
    list_ballots_workflow,
)
from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface


class TestListBallotsWorkflow(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.mock_repository = Mock(spec=BallotRepositoryInterface)

    def test_list_ballots_return_items(self):
        choice_item1 = ChoiceItem(
            id=self.fake.pyint(),
            name=self.fake.word(),
            description=self.fake.sentence()
        )
        ballot_item1 = BallotItem(
            id=self.fake.pyint(),
            title=self.fake.sentence(nb_words=3),
            slug=self.fake.slug(),
            description=self.fake.sentence(),
            choices=[choice_item1]
        )

        choice_item2 = ChoiceItem(
            id=self.fake.pyint(),
            name=self.fake.word(),
            description=self.fake.sentence()
        )
        ballot_item2 = BallotItem(
            id=self.fake.pyint(),
            title=self.fake.sentence(nb_words=3),
            slug=self.fake.slug(),
            description=self.fake.sentence(),
            choices=[choice_item2]
        )

        ballot_items = [ballot_item1, ballot_item2]
        self.mock_repository.list_ballots.return_value = ballot_items

        result = list_ballots_workflow(ballot_repository=self.mock_repository)

        self.mock_repository.list_ballots.assert_called_once()
        self.assertEqual(result, ballot_items)

    def test_list_ballots_return_empty_list(self):
        self.mock_repository.list_ballots.return_value = []

        result = list_ballots_workflow(ballot_repository=self.mock_repository)

        self.mock_repository.list_ballots.assert_called_once()
        self.assertEqual(result, [])