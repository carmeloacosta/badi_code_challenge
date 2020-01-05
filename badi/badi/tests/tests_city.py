#!/bin/python3


import os
from django.test import TestCase

from ..settings import FIXTURE_DIRS
from ..city import City
from ..constants import DEFAULT_CITY, DEFAULT_CITY_VALUES


class CityTestCase(TestCase):

    fixtures = [os.path.join(FIXTURE_DIRS[0], 'initial_state.json'), ]

    def setUp(self):
        pass

    def test__city_empty_creation__ok(self):
        city_info = []

        # Test main
        new_city = City(city_info)

        # Check results
        self.assertEqual(new_city.name, DEFAULT_CITY)  # Default name
        self.assertEqual(new_city.dawn, DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"])  # Default dawn time
        self.assertEqual(new_city.sunset, DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"])  # Default sunset time
