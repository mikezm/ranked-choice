# Update the import to use the full path
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase
from ranked_choice.core.models import Choice
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
        self.repository.create_ballot(title="Test Ballot")
        # Since create_ballot no longer returns a ballot, we need to retrieve it
        from django.utils.text import slugify
        slug = slugify("Test Ballot")
        ballot = self.repository.get_ballot_by_slug(slug)
        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")
        self.assertEqual(ballot.slug, "test-ballot")
        self.assertEqual(Choice.objects.filter(ballot=ballot).count(), 0)

    def test_create_ballot_with_title_and_description(self):
        """
        Test creating a ballot with a title and description.
        """
        self.repository.create_ballot(
            title="Test Ballot",
            description="This is a test ballot"
        )
        # Since create_ballot no longer returns a ballot, we need to retrieve it
        from django.utils.text import slugify
        slug = slugify("Test Ballot")
        ballot = self.repository.get_ballot_by_slug(slug)
        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")
        choices = Choice.objects.filter(ballot=ballot)
        self.assertEqual(choices.count(), 1)
        self.assertEqual(choices[0].description, "This is a test ballot")

    def test_get_ballot_by_id(self):
        """
        Test getting a ballot by ID.
        """
        self.repository.create_ballot(title="Test Ballot")
        # Since create_ballot no longer returns a ballot, we need to retrieve it
        from django.utils.text import slugify
        slug = slugify("Test Ballot")
        ballot = self.repository.get_ballot_by_slug(slug)
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
        self.repository.create_ballot(title="Test Ballot")
        # Since create_ballot no longer returns a ballot, we need to retrieve it
        from django.utils.text import slugify
        slug = slugify("Test Ballot")
        ballot = self.repository.get_ballot_by_slug(slug)
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
        self.repository.create_ballot(title="Test Ballot 1")
        self.repository.create_ballot(title="Test Ballot 2")
        # Since create_ballot no longer returns a ballot, we need to retrieve them
        from django.utils.text import slugify
        slug1 = slugify("Test Ballot 1")
        slug2 = slugify("Test Ballot 2")
        ballot1 = self.repository.get_ballot_by_slug(slug1)
        ballot2 = self.repository.get_ballot_by_slug(slug2)
        ballots = self.repository.list_ballots()
        self.assertEqual(len(ballots), 2)
        self.assertIn(ballot1, ballots)
        self.assertIn(ballot2, ballots)

    def test_create_ballot_with_choices(self):
        """
        Test creating a ballot with choices.
        """
        choices = [
            {"name": "Option 1", "description": "Description 1"},
            {"name": "Option 2", "description": "Description 2"}
        ]

        self.repository.create_ballot(
            title="Test Ballot",
            description="This is a test ballot",
            choices=choices
        )

        # Since create_ballot no longer returns a ballot, we need to retrieve it
        from django.utils.text import slugify
        slug = slugify("Test Ballot")
        ballot = self.repository.get_ballot_by_slug(slug)

        self.assertIsNotNone(ballot)
        self.assertEqual(ballot.title, "Test Ballot")

        # Check that all choices were created
        db_choices = Choice.objects.filter(ballot=ballot).order_by('name')
        self.assertEqual(db_choices.count(), 3)  # 2 choices + 1 description

        # Check the description choice
        description_choice = db_choices.get(name="Description")
        self.assertEqual(description_choice.description, "This is a test ballot")

        # Check the other choices
        option1 = db_choices.get(name="Option 1")
        self.assertEqual(option1.description, "Description 1")

        option2 = db_choices.get(name="Option 2")
        self.assertEqual(option2.description, "Description 2")