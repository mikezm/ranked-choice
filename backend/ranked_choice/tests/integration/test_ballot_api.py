import os
import unittest

# Add 'testserver' to ALLOWED_HOSTS for testing
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ranked_choice.core.models import Ballot, Choice
from ranked_choice.core.repositories.ballot_repository import BallotRepository as DjangoBallotRepository
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase


class BallotAPITests(IntegrationTestCase):
    """
    Tests for the ballot API endpoints.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        self.client = APIClient()
        self.create_ballot_url = reverse('api:create_ballot')
        self.repository = DjangoBallotRepository()

    def test_create_ballot_with_valid_data(self):
        """
        Test creating a ballot with valid data.
        """
        # Prepare data
        data = {
            'title': 'Test Ballot',
            'description': 'This is a test ballot'
        }

        # Make request
        response = self.client.post(self.create_ballot_url, data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('slug', response.data)
        self.assertIn('title', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        self.assertEqual(response.data['title'], 'Test Ballot')

        # Assert database state
        ballot = Ballot.objects.get(id=response.data['id'])
        self.assertEqual(ballot.title, 'Test Ballot')
        self.assertEqual(ballot.slug, 'test-ballot')

        # Assert that a choice was created with the description
        choices = Choice.objects.filter(ballot=ballot)
        self.assertEqual(choices.count(), 1)
        self.assertEqual(choices[0].name, 'Description')
        self.assertEqual(choices[0].description, 'This is a test ballot')

    def test_create_ballot_with_title_only(self):
        """
        Test creating a ballot with a title only.
        """
        # Prepare data
        data = {
            'title': 'Test Ballot'
        }

        # Make request
        response = self.client.post(self.create_ballot_url, data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('slug', response.data)
        self.assertIn('title', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        self.assertEqual(response.data['title'], 'Test Ballot')

        # Assert database state
        ballot = Ballot.objects.get(id=response.data['id'])
        self.assertEqual(ballot.title, 'Test Ballot')
        self.assertEqual(ballot.slug, 'test-ballot')

        # Assert that no choices were created
        choices = Choice.objects.filter(ballot=ballot)
        self.assertEqual(choices.count(), 0)

    def test_create_ballot_with_empty_title(self):
        """
        Test creating a ballot with an empty title.
        """
        # Prepare data
        data = {
            'title': '',
            'description': 'This is a test ballot'
        }

        # Make request
        response = self.client.post(self.create_ballot_url, data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_ballot_with_missing_title(self):
        """
        Test creating a ballot with a missing title.
        """
        # Prepare data
        data = {
            'description': 'This is a test ballot'
        }

        # Make request
        response = self.client.post(self.create_ballot_url, data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_ballot_with_choices(self):
        """
        Test creating a ballot with choices.
        """
        # Prepare data
        data = {
            'title': 'Test Ballot with Choices',
            'description': 'This is a test ballot with choices',
            'choices': [
                {'name': 'Option 1', 'description': 'Description 1'},
                {'name': 'Option 2', 'description': 'Description 2'}
            ]
        }

        # Make request
        response = self.client.post(self.create_ballot_url, data, format='json')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('slug', response.data)
        self.assertIn('title', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        self.assertEqual(response.data['title'], 'Test Ballot with Choices')

        # Assert database state
        ballot = Ballot.objects.get(id=response.data['id'])
        self.assertEqual(ballot.title, 'Test Ballot with Choices')
        self.assertEqual(ballot.slug, 'test-ballot-with-choices')

        # Assert that choices were created
        choices = Choice.objects.filter(ballot=ballot).order_by('name')
        self.assertEqual(choices.count(), 3)  # 2 choices + 1 description

        # Check the description choice
        description_choice = choices.get(name='Description')
        self.assertEqual(description_choice.description, 'This is a test ballot with choices')

        # Check the other choices
        option1 = choices.get(name='Option 1')
        self.assertEqual(option1.description, 'Description 1')

        option2 = choices.get(name='Option 2')
        self.assertEqual(option2.description, 'Description 2')


if __name__ == "__main__":
    unittest.main()