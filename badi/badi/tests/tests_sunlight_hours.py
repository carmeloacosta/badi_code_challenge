#!/bin/python3


from django.test import TestCase

from ..constants import DEFAULT_CITY, DEFAULT_CITY_VALUES
from ..sunlight_hours import get_apartment_dawn


class SunlightHoursTestCase(TestCase):

    def setUp(self):
        pass

    def test__get_apartment_dawn__ok(self):
        angle = 45.0

        # Test main
        apartment_dawn = get_apartment_dawn(angle, DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"],
                                            DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"])

        # Check results
        self.assertEqual(apartment_dawn, "09:45")
