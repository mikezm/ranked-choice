import unittest
from unittest.mock import Mock
from faker import Faker
from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface
from ranked_choice.core.domain.workflows.create_ballot_workflow import create_ballot_workflow
from django.utils.text import slugify


class TestCreateBallotWorkflow(unittest.TestCase):
    """
    Unit tests for ballot workflows.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        # Initialize Faker
        self.fake = Faker()
        
        # Test data
        self.mock_ballot_title = self.fake.sentence(nb_words=3)
        self.mock_ballot_slug = slugify(self.mock_ballot_title)
        self.mock_ballot_description = self.fake.paragraph()
        self.mock_choices = [
            {
                "name": self.fake.word(),
                "description": self.fake.sentence()
            }
        ]

        # Create a mock repository
        self.mock_repository = Mock(spec=BallotRepositoryInterface)
        # Configure create_ballot to return the slug
        self.mock_repository.create_ballot.return_value = self.mock_ballot_slug

    def test_create_new_ballot_with_valid_data(self):
        """
        Test creating a new ballot with valid data.
        """
        # Call the workflow and capture the return value
        slug = create_ballot_workflow(
            title=self.mock_ballot_title,
            choices=self.mock_choices,
            description=self.mock_ballot_description,
            ballot_repository=self.mock_repository
        )

        # Assert that the repository's create_ballot method was called with the correct arguments
        self.mock_repository.create_ballot.assert_called_once_with(
            self.mock_ballot_title, self.mock_choices, self.mock_ballot_description
        )

        # Assert that the correct slug is returned
        self.assertEqual(slug, self.mock_ballot_slug)

    def test_create_new_ballot_with_empty_title(self):
        """
        Test creating a new ballot with an empty title.
        """
        # Assert that calling the workflow with an empty title raises a ValueError
        with self.assertRaises(ValueError):
            create_ballot_workflow(
                ballot_repository=self.mock_repository,
                title="",
                choices=self.mock_choices,
                description=self.mock_ballot_description
            )

        # Assert that the repository's create_ballot method was not called
        self.mock_repository.create_ballot.assert_not_called()

    def test_create_new_ballot_without_description(self):
        """
        Test creating a new ballot without a description.
        """
        # Call the workflow and capture the return value
        slug = create_ballot_workflow(
            ballot_repository=self.mock_repository,
            title=self.mock_ballot_title,
            choices=self.mock_choices
        )

        # Assert that the repository's create_ballot method was called with the correct arguments
        self.mock_repository.create_ballot.assert_called_once_with(
            self.mock_ballot_title, self.mock_choices, None
        )

        # Assert that the correct slug is returned
        self.assertEqual(slug, self.mock_ballot_slug)

    def test_create_new_ballot_with_choices(self):
        """
        Test creating a new ballot with choices.
        """
        extended_choices = [
            {
                "name": self.fake.word(),
                "description": self.fake.sentence()
            },
            {
                "name": self.fake.word(),
                "description": self.fake.sentence()
            }
        ]

        # Call the workflow and capture the return value
        slug = create_ballot_workflow(
            ballot_repository=self.mock_repository,
            title=self.mock_ballot_title,
            choices=extended_choices,
            description=self.mock_ballot_description
        )

        # Assert that the repository's create_ballot method was called with the correct arguments
        self.mock_repository.create_ballot.assert_called_once_with(
            self.mock_ballot_title, extended_choices, self.mock_ballot_description
        )

        # Assert that the correct slug is returned
        self.assertEqual(slug, self.mock_ballot_slug)

    def test_create_new_ballot_with_empty_choices(self):
        """
        Test creating a new ballot with empty choices.
        """
        # Assert that calling the workflow with empty choices raises a ValueError
        with self.assertRaises(ValueError):
            create_ballot_workflow(
                ballot_repository=self.mock_repository,
                title=self.mock_ballot_title,
                choices=[],
                description=self.mock_ballot_description
            )

        # Assert that the repository's create_ballot method was not called
        self.mock_repository.create_ballot.assert_not_called()


if __name__ == "__main__":
    unittest.main()