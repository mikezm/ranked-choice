import os
import unittest

from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase

os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'

class CreateVoteAPITests(IntegrationTestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_vote_url = reverse('api:create_vote')
        self.repository = BallotRepository()
        self.fake = Faker()

    def test_create_vote_with_valid_data(self):
        slug = self.repository.create_ballot(
            title='Test Ballot',
            choices=[
                {'name': 'Option 1', 'description': 'Description 1'},
                {'name': 'Option 2', 'description': 'Description 2'},
            ]
        )
        ballot_item = self.repository.get_ballot_by_slug(slug)
        data = {
            'name': 'test voter',
            'ballot_id': ballot_item.id,
            'votes': [
                {'rank': 1, 'choice_id': ballot_item.choices[0].id},
                {'rank': 2, 'choice_id': ballot_item.choices[1].id},
            ]
        }

        response = self.client.post(self.create_vote_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vote_without_votes(self):
        data = {
            'name': 'test voter',
            'ballot_id': self.fake.pyint(),
            'votes': []
        }

        response = self.client.post(self.create_vote_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == "__main__":
    unittest.main()