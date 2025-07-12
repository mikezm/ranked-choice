import unittest
from unittest.mock import Mock

from django.utils.text import slugify
from faker import Faker

from ranked_choice.core.domain.items.ballot_item import BallotItem, ChoiceItem
from ranked_choice.core.domain.workflows.list_ballots_workflow import list_ballots_workflow
from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface


class TestListBallotsWorkflow(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment.
        """
        self.fake = Faker()
        self.mock_repository = Mock(spec=BallotRepositoryInterface)

    def test_list_ballots_return_items(self):
        """
        Test that list_ballots_workflow returns the list of ballot items from the repository.
        """
        # Create test data
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

        # Configure mock repository
        self.mock_repository.list_ballots.return_value = ballot_items

        # Call the workflow
        result = list_ballots_workflow(ballot_repository=self.mock_repository)

        # Assert that the repository method was called
        self.mock_repository.list_ballots.assert_called_once()

        # Assert that the workflow returned the expected result
        self.assertEqual(result, ballot_items)

    def test_list_ballots_return_empty_list(self):
        """
        Test that list_ballots_workflow returns an empty list when the repository returns an empty list.
        """
        # Configure mock repository
        self.mock_repository.list_ballots.return_value = []

        # Call the workflow
        result = list_ballots_workflow(ballot_repository=self.mock_repository)

        # Assert that the repository method was called
        self.mock_repository.list_ballots.assert_called_once()

        # Assert that the workflow returned an empty list
        self.assertEqual(result, [])