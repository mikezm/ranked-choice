from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase


class TestBallotRepository(IntegrationTestCase):
    """
    Integration tests for the Django ballot repository.
    """

    def setUp(self):
        """
        Set up each test.
        """
        self.repository = BallotRepository()

    def test_create_ballot_with_title_only(self):
        """
        Test creating a ballot with a title and required choices, but no description.
        """
        choices = [
            {"name": "Option 1", "description": "Description 1"}
        ]
        slug = self.repository.create_ballot(title="Test Ballot", choices=choices)
        # Verify the returned slug
        self.assertTrue(slug.startswith("test-ballot"))
        ballot = self.repository.get_ballot_by_slug(slug)
        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")
        self.assertTrue(ballot.slug.startswith("test-ballot"))
        self.assertEqual(len(ballot.choices), 1)
        self.assertEqual(ballot.choices[0].name, "Option 1")
        self.assertEqual(ballot.choices[0].description, "Description 1")

    def test_create_ballot_with_title_and_description(self):
        """
        Test creating a ballot with a title, description, and required choices.
        """
        choices = [
            {"name": "Option 1", "description": "Description 1"}
        ]
        slug = self.repository.create_ballot(
            title="Test Ballot",
            choices=choices,
            description="This is a test ballot"
        )
        # Verify the returned slug
        self.assertTrue(slug.startswith("test-ballot"))
        ballot = self.repository.get_ballot_by_slug(slug)
        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")
        self.assertEqual(ballot.description, "This is a test ballot")
        self.assertEqual(len(ballot.choices), 1)
        self.assertEqual(ballot.choices[0].name, "Option 1")
        self.assertEqual(ballot.choices[0].description, "Description 1")


    def test_get_ballot_by_slug(self):
        """
        Test getting a ballot by slug.
        """
        choices = [
            {"name": "Option 1", "description": "Description 1"}
        ]
        slug = self.repository.create_ballot(title="Test Ballot", choices=choices)
        # Verify the returned slug
        self.assertTrue(slug.startswith("test-ballot"))
        ballot = self.repository.get_ballot_by_slug(slug)
        retrieved_ballot = self.repository.get_ballot_by_slug(ballot.slug)
        self.assertIsNotNone(retrieved_ballot)
        self.assertEqual(retrieved_ballot.slug, ballot.slug)
        self.assertEqual(retrieved_ballot.title, ballot.title)
        self.assertEqual(len(retrieved_ballot.choices), 1)
        self.assertEqual(retrieved_ballot.choices[0].name, "Option 1")
        self.assertEqual(retrieved_ballot.choices[0].description, "Description 1")

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
        choices1 = [
            {"name": "Option 1", "description": "Description 1"}
        ]
        choices2 = [
            {"name": "Option 2", "description": "Description 2"}
        ]
        slug1 = self.repository.create_ballot(title="Test Ballot 1", choices=choices1)
        slug2 = self.repository.create_ballot(title="Test Ballot 2", choices=choices2)

        # Verify the returned slugs
        self.assertTrue(slug1.startswith("test-ballot-1"))
        self.assertTrue(slug2.startswith("test-ballot-2"))

        ballots = self.repository.list_ballots()
        self.assertEqual(len(ballots), 2)

        # Find ballots by slug
        ballot1 = next((b for b in ballots if b.slug == slug1), None)
        ballot2 = next((b for b in ballots if b.slug == slug2), None)

        self.assertIsNotNone(ballot1)
        self.assertIsNotNone(ballot2)
        self.assertEqual(ballot1.title, "Test Ballot 1")
        self.assertEqual(ballot2.title, "Test Ballot 2")
        self.assertEqual(len(ballot1.choices), 1)
        self.assertEqual(len(ballot2.choices), 1)
        self.assertEqual(ballot1.choices[0].name, "Option 1")
        self.assertEqual(ballot2.choices[0].name, "Option 2")

    def test_create_ballot_with_choices(self):
        """
        Test creating a ballot with choices.
        """
        choices = [
            {"name": "Option 1", "description": "Description 1"},
            {"name": "Option 2", "description": "Description 2"}
        ]

        slug = self.repository.create_ballot(
            title="Test Ballot",
            choices=choices,
            description="This is a test ballot"
        )

        # Verify the returned slug
        self.assertTrue(slug.startswith("test-ballot"))
        ballot = self.repository.get_ballot_by_slug(slug)

        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")
        self.assertTrue(ballot.slug.startswith("test-ballot"))
        self.assertEqual(ballot.description, "This is a test ballot")

        # Check that all choices were created
        self.assertEqual(len(ballot.choices), 2)

        # Find choices by name
        option1 = next((c for c in ballot.choices if c.name == "Option 1"), None)
        option2 = next((c for c in ballot.choices if c.name == "Option 2"), None)

        self.assertIsNotNone(option1)
        self.assertIsNotNone(option2)
        self.assertEqual(option1.description, "Description 1")
        self.assertEqual(option2.description, "Description 2")

    def test_create_voter_with_votes(self):
        choices = [
            {"name": "Option 1", "description": "Description 1"},
            {"name": "Option 2", "description": "Description 2"}
        ]

        slug = self.repository.create_ballot(
            title="Test Ballot",
            choices=choices,
            description="This is a test ballot"
        )

        ballot_item = self.repository.get_ballot_by_slug(slug)

        voter = "voter name"
        votes = [{
            "rank": index,
            "choice_id": choice.id
        } for index, choice in enumerate(ballot_item.choices)]

        self.repository.create_voter(name=voter, ballot_id=ballot_item.id, votes=votes)
        vote_items = self.repository.get_votes_by_ballot_id(ballot_id=ballot_item.id)

        self.assertEqual(len(vote_items), 1)
        self.assertEqual(len(vote_items[0].votes), 2)
        self.assertEqual(vote_items[0].name, voter)
        self.assertEqual(vote_items[0].votes[0].rank, 0)
        self.assertEqual(vote_items[0].votes[0].choice_id, ballot_item.choices[0].id)
        self.assertEqual(vote_items[0].votes[1].rank, 1)
        self.assertEqual(vote_items[0].votes[1].choice_id, ballot_item.choices[1].id)