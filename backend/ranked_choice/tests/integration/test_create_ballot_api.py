import os
import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ranked_choice.core.models import Ballot, Choice
from ranked_choice.core.repositories.ballot_repository import (
    BallotRepository as DjangoBallotRepository,
)
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase

os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'


class CreateBallotAPITests(IntegrationTestCase):
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
        data = {
            'title': 'Test Ballot',
            'description': 'This is a test ballot',
            'choices': [
                {'name': 'Option 1', 'description': 'Description 1'}
            ]
        }

        response = self.client.post(self.create_ballot_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('slug', response.data)
        self.assertTrue(response.data['slug'].startswith('test-ballot'))

        ballot = Ballot.objects.get(slug=response.data['slug'])
        self.assertEqual(ballot.title, 'Test Ballot')
        self.assertTrue(ballot.slug.startswith('test-ballot'))

        choices = Choice.objects.filter(ballot=ballot).order_by('name')
        self.assertEqual(choices.count(), 1)  # 1 choice + 1 description

        option1 = choices.get(name='Option 1')
        self.assertEqual(option1.description, 'Description 1')

    def test_create_ballot_with_title_only(self):
        """
        Test creating a ballot with a title only.
        """
        data = {
            'title': 'Test Ballot'
        }

        response = self.client.post(self.create_ballot_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('choices', response.data)

    def test_create_ballot_with_empty_choices(self):
        """
        Test creating a ballot with empty choices list.
        """
        data = {
            'title': 'Test Ballot',
            'choices': []
        }

        response = self.client.post(self.create_ballot_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('choices', response.data)

    def test_create_ballot_with_empty_title(self):
        """
        Test creating a ballot with an empty title.
        """
        data = {
            'title': '',
            'description': 'This is a test ballot'
        }

        response = self.client.post(self.create_ballot_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_ballot_with_missing_title(self):
        """
        Test creating a ballot with a missing title.
        """
        data = {
            'description': 'This is a test ballot'
        }

        response = self.client.post(self.create_ballot_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_ballot_with_choices(self):
        """
        Test creating a ballot with choices.
        """
        data = {
            'title': 'Test Ballot with Choices',
            'description': 'This is a test ballot with choices',
            'choices': [
                {'name': 'Option 1', 'description': 'Description 1'},
                {'name': 'Option 2', 'description': 'Description 2'}
            ]
        }

        response = self.client.post(self.create_ballot_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('slug', response.data)
        self.assertTrue(response.data['slug'].startswith('test-ballot-with-choices'))

        ballot = Ballot.objects.get(slug=response.data['slug'])
        self.assertEqual(ballot.title, 'Test Ballot with Choices')
        self.assertTrue(ballot.slug.startswith( 'test-ballot-with-choices'))

        choices = Choice.objects.filter(ballot=ballot).order_by('name')
        self.assertEqual(choices.count(), 2)

        option1 = choices.get(name='Option 1')
        self.assertEqual(option1.description, 'Description 1')

        option2 = choices.get(name='Option 2')
        self.assertEqual(option2.description, 'Description 2')


if __name__ == "__main__":
    unittest.main()
