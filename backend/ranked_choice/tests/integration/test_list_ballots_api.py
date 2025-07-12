import os
import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ranked_choice.core.models import Ballot, Choice
from ranked_choice.core.repositories.ballot_repository import BallotRepository
from ranked_choice.tests.integration.integration_test_case import IntegrationTestCase

os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'


class ListBallotsAPITests(IntegrationTestCase):
    """
    Tests for the list_ballots API endpoint.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.repository = BallotRepository()

        self.test_ballot1 = Ballot.objects.create(
            title="Test Ballot 1",
            description="This is test ballot 1",
            slug="test-ballot-1"
        )

        Choice.objects.create(
            ballot=self.test_ballot1,
            name="Option 1",
            description="Description 1"
        )
        Choice.objects.create(
            ballot=self.test_ballot1,
            name="Option 2",
            description="Description 2"
        )

        self.test_ballot2 = Ballot.objects.create(
            title="Test Ballot 2",
            description="This is test ballot 2",
            slug="test-ballot-2"
        )

        Choice.objects.create(
            ballot=self.test_ballot2,
            name="Option A",
            description="Description A"
        )
        Choice.objects.create(
            ballot=self.test_ballot2,
            name="Option B",
            description="Description B"
        )

        self.list_ballots_url = reverse('api:list_ballots')

    def test_list_ballots_success(self):
        response = self.client.get(self.list_ballots_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        ballots = sorted(response.data, key=lambda x: x['title'])

        self.assertEqual(ballots[0]['title'], "Test Ballot 1")
        self.assertEqual(ballots[0]['description'], "This is test ballot 1")
        self.assertEqual(ballots[0]['slug'], "test-ballot-1")
        self.assertEqual(len(ballots[0]['choices']), 2)

        choices1 = sorted(ballots[0]['choices'], key=lambda x: x['name'])
        self.assertEqual(choices1[0]['name'], "Option 1")
        self.assertEqual(choices1[0]['description'], "Description 1")
        self.assertEqual(choices1[1]['name'], "Option 2")
        self.assertEqual(choices1[1]['description'], "Description 2")

        self.assertEqual(ballots[1]['title'], "Test Ballot 2")
        self.assertEqual(ballots[1]['description'], "This is test ballot 2")
        self.assertEqual(ballots[1]['slug'], "test-ballot-2")
        self.assertEqual(len(ballots[1]['choices']), 2)

        choices2 = sorted(ballots[1]['choices'], key=lambda x: x['name'])
        self.assertEqual(choices2[0]['name'], "Option A")
        self.assertEqual(choices2[0]['description'], "Description A")
        self.assertEqual(choices2[1]['name'], "Option B")
        self.assertEqual(choices2[1]['description'], "Description B")

    def test_list_ballots_empty(self):
        Ballot.objects.all().delete()

        response = self.client.get(self.list_ballots_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


if __name__ == "__main__":
    unittest.main()