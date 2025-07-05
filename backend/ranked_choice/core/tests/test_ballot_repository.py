import os

# Import the IntegrationTestCase
from ranked_choice.core.tests.integration_test_case import IntegrationTestCase
from ranked_choice.core.models import Ballot, Choice
from ranked_choice.core.repositories.ballot_repository import BallotRepository


class TestDjangoBallotRepository(IntegrationTestCase):
    """
    Integration tests for the Django ballot repository.
    """

    def setUp(self):
        """
        Set up each test.
        """
        self.repository = BallotRepository()
        # No manual data clearing is needed; Django's TestCase wraps each
        # test in a transaction and rolls it back afterward.

    def test_create_ballot_with_title_only(self):
        """
        Test creating a ballot with a title only.
        """
        ballot = self.repository.create_ballot(title="Test Ballot")
        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")
        self.assertEqual(ballot.slug, "test-ballot")
        self.assertEqual(Choice.objects.filter(ballot=ballot).count(), 0)

    def test_create_ballot_with_title_and_description(self):
        """
        Test creating a ballot with a title and description.
        """
        ballot = self.repository.create_ballot(
            title="Test Ballot",
            description="This is a test ballot"
        )
        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")
        choices = Choice.objects.filter(ballot=ballot)
        self.assertEqual(choices.count(), 1)
        self.assertEqual(choices[0].description, "This is a test ballot")

    def test_get_ballot_by_id(self):
        """
        Test getting a ballot by ID.
        """
        ballot = self.repository.create_ballot(title="Test Ballot")
        retrieved_ballot = self.repository.get_ballot_by_id(ballot.id)
        self.assertIsNotNone(retrieved_ballot)
        self.assertEqual(retrieved_ballot.id, ballot.id)

    def test_get_ballot_by_id_nonexistent(self):
        """
        Test getting a nonexistent ballot by ID.
        """
        retrieved_ballot = self.repository.get_ballot_by_id(999)
        self.assertIsNone(retrieved_ballot)

    def test_get_ballot_by_slug(self):
        """
        Test getting a ballot by slug.
        """
        ballot = self.repository.create_ballot(title="Test Ballot")
        retrieved_ballot = self.repository.get_ballot_by_slug(ballot.slug)
        self.assertIsNotNone(retrieved_ballot)
        self.assertEqual(retrieved_ballot.slug, ballot.slug)

    def test_get_ballot_by_slug_nonexistent(self):
        """
        Test getting a nonexistent ballot by slug.
        """
        retrieved_ballot = self.repository.get_ballot_by_slug("nonexistent-ballot")
        self.assertIsNone(retrieved_ballot)

    def test_list_ballots(self):
        """
        Test listing all ballots.
        """
        ballot1 = self.repository.create_ballot(title="Test Ballot 1")
        ballot2 = self.repository.create_ballot(title="Test Ballot 2")
        ballots = self.repository.list_ballots()
        self.assertEqual(len(ballots), 2)
        self.assertIn(ballot1, ballots)
        self.assertIn(ballot2, ballots)
