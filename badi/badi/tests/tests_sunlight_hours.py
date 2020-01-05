#!/bin/python3


from django.test import TestCase

from ..constants import DEFAULT_CITY, DEFAULT_CITY_VALUES
from ..sunlight_hours import get_apartment_dawn, get_apartment_sunset


class SunlightHoursTestCase(TestCase):

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
