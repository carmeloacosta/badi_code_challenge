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

    def test__city_initialization__ok(self):

        #[{ neighborhood: <name_string>, apartments_height: <number>, buildings: [{name:
        #<name_string>, apartments_count: <number>, distance: <number>}]}]
        city_info = [
            {"neighborhood": "POBLENOU", "apartments_height": 1, "buildings":
                [{"name": "Aticco", "apartments_count": 8, "distance": 1},
                 {"name": "01", "apartments_count": 4, "distance": 2},
                 {"name": "CEM", "apartments_count": 7, "distance": 1},
                 {"name": "30", "apartments_count": 1, "distance": -1}
                 ]
             },
            {"neighborhood": "RAVAL", "apartments_height": 2, "buildings":
                [{"name": "Santa Monica", "apartments_count": 3, "distance": 1},
                 {"name": "La Capella", "apartments_count": 2, "distance": 1},
                 {"name": "CCCB", "apartments_count": 4, "distance": -1}
                 ]
             }
        ]

        #[{ neighborhood: <name_string>, apartments_height: <number>, buildings: [{name:
        #<name_string>, apartments_count: <number>, distance: <number>}]}]
        expected_city_info = [
            {"neighborhood": "POBLENOU", "apartments_height": 1, "buildings":
                [{"name": "Aticco", "apartments_count": 8, "distance": 1},
                 {"name": "01", "apartments_count": 4, "distance": 2},
                 {"name": "CEM", "apartments_count": 7, "distance": 1},
                 {"name": "30", "apartments_count": 1, "distance": -1}
                 ]
             },
            {"neighborhood": "RAVAL", "apartments_height": 2, "buildings":
                [{"name": "Santa Monica", "apartments_count": 3, "distance": 1},
                 {"name": "La Capella", "apartments_count": 2, "distance": 1},
                 {"name": "CCCB", "apartments_count": 4, "distance": -1}
                 ]
             }
        ]

        # Test main
        new_city = City(city_info)

        # Check results
        self.assertEqual(new_city.name, DEFAULT_CITY)  # Default name
        self.assertEqual(new_city.dawn, DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"])  # Default dawn time
        self.assertEqual(new_city.sunset, DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"])  # Default sunset time
