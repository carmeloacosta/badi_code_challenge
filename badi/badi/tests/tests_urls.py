#!/bin/python3


import os
from json import dumps
from django.test import TestCase

from ..settings import FIXTURE_DIRS


class InitViewTestCase(TestCase):

    fixtures = [os.path.join(FIXTURE_DIRS[0], 'initial_state.json'), ]

    def setUp(self):
        pass

    def test__empty_init__ok(self):
        body = []

        response = self.client.post('/init',
                                    dumps(body),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Barcelona city updated")
