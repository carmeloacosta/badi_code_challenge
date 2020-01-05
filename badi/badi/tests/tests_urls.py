import os
from django.test import TestCase

from ..settings import FIXTURE_DIRS


class InitViewTestCase(TestCase):

    fixtures = [os.path.join(FIXTURE_DIRS[0], 'initial_state.json'), ]

    def setUp(self):
        pass

    def test__init__ok(self):
        response = self.client.get("/init")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Barcelona city updated")
