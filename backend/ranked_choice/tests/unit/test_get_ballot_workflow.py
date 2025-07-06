import unittest
from unittest.mock import Mock

from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface


class TestGetBallotWorkflow(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment.
        """

        # Create a mock repository
        self.mock_repository = Mock(spec=BallotRepositoryInterface)
        # Configure create_ballot to return the slug
        self.mock_repository.create_ballot.return_value = "test-ballot"