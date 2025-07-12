import os
import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase

os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'


class GetVotesAPITests(IntegrationTestCase):
    def setUp(self):
        self.client = APIClient()
        self.repository = BallotRepository()
        self.fake_ballot_slug = 'nonexistent-ballot'

    def test_get_votes_with_valid_slug(self):
        # Create a test ballot
        slug = self.repository.create_ballot(
            title='Test Ballot for Votes',
            choices=[
                {'name': 'Option 1', 'description': 'Description 1'},
                {'name': 'Option 2', 'description': 'Description 2'},
                {'name': 'Option 3', 'description': 'Description 3'},
            ]
        )

        # Get the ballot to access its ID and choices
        ballot_item = self.repository.get_ballot_by_slug(slug)

        # Create votes for the ballot
        self.repository.create_voter(
            name='Voter 1',
            ballot_id=ballot_item.id,
            votes=[
                {'rank': 1, 'choice_id': ballot_item.choices[0].id},
                {'rank': 2, 'choice_id': ballot_item.choices[1].id},
                {'rank': 3, 'choice_id': ballot_item.choices[2].id},
            ]
        )

        self.repository.create_voter(
            name='Voter 2',
            ballot_id=ballot_item.id,
            votes=[
                {'rank': 1, 'choice_id': ballot_item.choices[0].id},
                {'rank': 2, 'choice_id': ballot_item.choices[2].id},
                {'rank': 3, 'choice_id': ballot_item.choices[1].id},
            ]
        )

        # Call the API endpoint
        url = reverse('api:get_votes', kwargs={'slug': slug})
        response = self.client.get(url)

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the expected fields
        self.assertIn('winner_id', response.data)
        self.assertIn('winner_name', response.data)
        self.assertIn('title', response.data)
        self.assertIn('rounds', response.data)

        # Verify the winner is Option 1 (which received all first-place votes)
        self.assertEqual(response.data['winner_name'], 'Option 1')
        self.assertEqual(response.data['title'], 'Test Ballot for Votes')

        # Verify rounds data exists
        self.assertTrue(len(response.data['rounds']) > 0)

    def test_get_votes_with_invalid_slug(self):
        # Call the API endpoint with a non-existent slug
        url = reverse('api:get_votes', kwargs={'slug': self.fake_ballot_slug})
        response = self.client.get(url)

        # Verify the response is a 200 OK (the workflow returns a default BallotResultItem)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response indicates no ballot was found
        self.assertEqual(response.data['winner_id'], -1)
        self.assertEqual(response.data['winner_name'], 'No ballot found')
        self.assertEqual(response.data['title'], '')
        self.assertEqual(response.data['rounds'], [])


if __name__ == "__main__":
    unittest.main()
