import unittest
from unittest.mock import Mock
from ranked_choice.core.models import Ballot
from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface
from ranked_choice.core.domain.workflows.create_ballot_workflow import create_ballot_workflow


class TestGetBallotWorkflow(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment.
        """

        # Create a mock repository
        self.mock_repository = Mock(spec=BallotRepositoryInterface)
        # Configure create_ballot to return the slug
        self.mock_repository.create_ballot.return_value = "test-ballot"