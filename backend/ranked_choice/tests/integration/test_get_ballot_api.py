import os
import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ranked_choice.core.models import Ballot, Choice
from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase

os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'


class GetBallotAPITests(IntegrationTestCase):
    """
    Tests for the get_ballot API endpoint.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        super().setUp()
        self.client = APIClient()
        self.repository = BallotRepository()

        # Create a test ballot to retrieve
        self.test_ballot = Ballot.objects.create(
            title="Test Ballot",
            description="This is a test ballot",
            slug="test-ballot"
        )

        # Create some choices for the test ballot
        Choice.objects.create(
            ballot=self.test_ballot,
            name="Option 1",
            description="Description 1"
        )
        Choice.objects.create(
            ballot=self.test_ballot,
            name="Option 2",
            description="Description 2"
        )

        # URL for retrieving the test ballot
        self.get_ballot_url = reverse(
            'api:get_ballot',
            kwargs={'slug': self.test_ballot.slug}
        )

        # URL for a non-existent ballot
        self.nonexistent_ballot_url = reverse(
            'api:get_ballot',
            kwargs={'slug': 'nonexistent-ballot'}
        )

    def test_get_ballot_success(self):
        """
        Test retrieving a ballot that exists.
        """
        response = self.client.get(self.get_ballot_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Ballot")
        self.assertEqual(response.data['description'], "This is a test ballot")
        self.assertEqual(response.data['slug'], "test-ballot")

        self.assertEqual(len(response.data['choices']), 2)

        choices = sorted(response.data['choices'], key=lambda x: x['name'])
        self.assertEqual(choices[0]['name'], "Option 1")
        self.assertEqual(choices[0]['description'], "Description 1")
        self.assertEqual(choices[1]['name'], "Option 2")
        self.assertEqual(choices[1]['description'], "Description 2")

    def test_get_nonexistent_ballot(self):
        """
        Test retrieving a ballot that doesn't exist.
        """
        response = self.client.get(self.nonexistent_ballot_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Ballot not found")

    def test_get_ballot_with_invalid_slug(self):
        """
        Test retrieving a ballot with an invalid slug format.
        """
        response = self.client.get('/api/ballots/invalid-slug/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)


if __name__ == "__main__":
    unittest.main()
