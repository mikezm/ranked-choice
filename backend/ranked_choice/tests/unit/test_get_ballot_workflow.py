import unittest
from unittest.mock import Mock

from ranked_choice.core.domain.items.ballot_item import BallotItem, ChoiceItem
from ranked_choice.core.domain.workflows.get_ballot_workflow import get_ballot_workflow
from django.utils.text import slugify
from faker import Faker

from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface


class TestGetBallotWorkflow(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment.
        """

        self.fake = Faker()
        self.mock_repository = Mock(spec=BallotRepositoryInterface)

    def test_get_ballot_return_item(self):
        title = self.fake.sentence(nb_words=3)
        slug = slugify(title)
        choice_item = ChoiceItem(
            name=self.fake.word(),
            description=self.fake.sentence()
        )
        ballot_item = BallotItem(
            title=title,
            slug=slug,
            description=self.fake.sentence(),
            choices=[choice_item]
        )

        self.mock_repository.get_ballot_by_slug.return_value = ballot_item

        result = get_ballot_workflow(slug=slug, ballot_repository=self.mock_repository)

        self.mock_repository.get_ballot_by_slug.assert_called_once_with(slug=slug)
        self.assertEqual(result, ballot_item)

    def test_get_ballot_return_none(self):
        slug = self.fake.slug()
        self.mock_repository.get_ballot_by_slug.return_value = None

        result = get_ballot_workflow(slug=slug, ballot_repository=self.mock_repository)

        self.mock_repository.get_ballot_by_slug.assert_called_once_with(slug=slug)
        self.assertIsNone(result)
