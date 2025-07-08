import unittest
from unittest.mock import Mock

from faker import Faker

from ranked_choice.core.domain.workflows.create_vote_workflow import (
    create_vote_workflow,
)
from ranked_choice.core.repositories.ballot_repository import BallotRepositoryInterface


class TestGetBallotWorkflow(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.mock_repository = Mock(spec=BallotRepositoryInterface)

    def test_create_voter(self):
        name = self.fake.name()
        ballot_id = self.fake.pyint()
        votes = [
            {"rank": 1, "choice_id": self.fake.pyint()},
            {"rank": 2, "choice_id": self.fake.pyint()},
        ]

        create_vote_workflow(
            name=name,
            ballot_id=ballot_id,
            votes=votes,
            ballot_repository=self.mock_repository
        )

        self.mock_repository.create_voter.assert_called_once_with(
            name=name,
            ballot_id=ballot_id,
            votes=votes,
        )

    def test_create_voter_with_no_votes(self):
        name = self.fake.name()
        ballot_id = self.fake.pyint()

        create_vote_workflow(
            name=name,
            ballot_id=ballot_id,
            votes=[],
            ballot_repository=self.mock_repository
        )

        self.mock_repository.create_voter.assert_not_called()
