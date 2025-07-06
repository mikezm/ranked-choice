import unittest
from unittest.mock import Mock
from ranked_choice.core.models import Ballot
from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface
from ranked_choice.core.domain.workflows.create_ballot_workflow import create_ballot_workflow


class TestBallotWorkflows(unittest.TestCase):
    """
    Unit tests for ballot workflows.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        # Create a mock ballot
        self.mock_ballot = Mock(spec=Ballot)
        self.mock_ballot.id = 1
        self.mock_ballot.slug = "test-ballot"
        self.mock_ballot.title = "Test Ballot"

        # Create a mock repository
        self.mock_repository = Mock(spec=BallotRepositoryInterface)
        # No return value for create_ballot as it now returns None

    def test_create_new_ballot_with_valid_data(self):
        """
        Test creating a new ballot with valid data.
        """
        # Call the workflow and capture the return value
        slug = create_ballot_workflow(
            ballot_repository=self.mock_repository,
            title="Test Ballot",
            description="This is a test ballot"
        )

        # Assert that the repository's create_ballot method was called with the correct arguments
        self.mock_repository.create_ballot.assert_called_once_with(
            "Test Ballot", "This is a test ballot", None
        )

        # Assert that the correct slug is returned
        self.assertEqual(slug, "test-ballot")

    def test_create_new_ballot_with_empty_title(self):
        """
        Test creating a new ballot with an empty title.
        """
        # Assert that calling the workflow with an empty title raises a ValueError
        with self.assertRaises(ValueError):
            create_ballot_workflow(
                ballot_repository=self.mock_repository,
                title="",
                description="This is a test ballot"
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
            title="Test Ballot"
        )

        # Assert that the repository's create_ballot method was called with the correct arguments
        self.mock_repository.create_ballot.assert_called_once_with(
            "Test Ballot", None, None
        )

        # Assert that the correct slug is returned
        self.assertEqual(slug, "test-ballot")

    def test_create_new_ballot_with_choices(self):
        """
        Test creating a new ballot with choices.
        """
        # Define choices
        choices = [
            {"name": "Option 1", "description": "Description 1"},
            {"name": "Option 2", "description": "Description 2"}
        ]

        # Call the workflow and capture the return value
        slug = create_ballot_workflow(
            ballot_repository=self.mock_repository,
            title="Test Ballot",
            description="This is a test ballot",
            choices=choices
        )

        # Assert that the repository's create_ballot method was called with the correct arguments
        self.mock_repository.create_ballot.assert_called_once_with(
            "Test Ballot", "This is a test ballot", choices
        )

        # Assert that the correct slug is returned
        self.assertEqual(slug, "test-ballot")


if __name__ == "__main__":
    unittest.main()
