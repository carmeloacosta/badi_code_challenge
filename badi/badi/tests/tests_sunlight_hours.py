#!/bin/python3


from django.test import TestCase

from ..constants import DEFAULT_CITY, DEFAULT_CITY_VALUES
from ..sunlight_hours import get_apartment_dawn, get_apartment_sunset, get_neighbourhood_sunlight_hours


class SunlightHoursTestCase(TestCase):

    maxDiff = None

    def setUp(self):
        pass

    def test__get_apartment_dawn__ok(self):
        angle = 22.25
        city_seconds_per_grade = 180

        # Test main
        apartment_dawn = get_apartment_dawn(angle, city_seconds_per_grade, DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"])

        # Check results
        self.assertEqual(apartment_dawn, "09:20")

    def test__get_apartment_sunset__ok(self):
        angle = 22.25
        city_seconds_per_grade = 180

        # Test main
        apartment_dawn = get_apartment_sunset(angle, city_seconds_per_grade,
                                              DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"])

        # Check results
        self.assertEqual(apartment_dawn, "16:19")

    def test__get_neighbourhood_sunlight_hours__ok(self):
        building_list = [{"name": "Aticco", "apartments_count": 8, "distance": 1},
                         {"name": "01", "apartments_count": 4, "distance": 2},
                         {"name": "CEM", "apartments_count": 7, "distance": 1},
                         {"name": "30", "apartments_count": 1, "distance": -1}]

        # Test main
        get_neighbourhood_sunlight_hours(building_list)

        # Check results
        expected_building_list = [
            {"name": "Aticco", "apartments_count": 8, "distance": 1,
             "dawn": [],
             "sunset": []
             },
            {"name": "01", "apartments_count": 4, "distance": 2,
             "dawn": [],
             "sunset": []
             },
            {"name": "CEM", "apartments_count": 7, "distance": 1,
             "dawn": [],
             "sunset": []
             },
            {"name": "30", "apartments_count": 1, "distance": -1,
             "dawn": [],
             "sunset": []
             }
        ]

        self.assertEqual(building_list, expected_building_list)
