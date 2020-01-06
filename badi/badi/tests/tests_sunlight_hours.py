#!/bin/python3


from django.test import TestCase

from ..constants import DEFAULT_CITY, DEFAULT_CITY_VALUES
from ..sunlight_hours import get_apartment_dawn, get_apartment_sunset, elapsed_time, get_max_west_shadow_details, \
    get_neighbourhood_sunlight_hours


class SunlightHoursTestCase(TestCase):

    maxDiff = None

    def setUp(self):
        pass

    def test__get_apartment_dawn__ok(self):
        # (<angle>, (<city_seconds_per_grade>, <expected_apartment_dawn>))
        values = [
            (22.25, 180, "09:20"),
            (76.0, 180, "12:02"),
        ]

        # Test main
        for value in values:
            apartment_dawn = get_apartment_dawn(value[0], value[1], DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"])

            # Check results
            self.assertEqual(apartment_dawn, value[2])

    def test__get_apartment_sunset__ok(self):
        # (<angle>, (<city_seconds_per_grade>, <expected_apartment_sunset>))
        values = [
            (170, 180, "08:55"),
            (22.25, 180, "16:19"),
            (46.0, 180, "15:07"),
        ]

        # Test main
        for value in values:
            apartment_dawn = get_apartment_sunset(value[0], value[1], DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"])

            # Check results
            self.assertEqual(apartment_dawn, value[2])

    def test__elapsed_time__ok(self):
        values = [
                    ("10:00", "17:00", (7, 0)),
                    ("9:59", "17:00", (7, 1)),
                ]

        # Test main
        for value in values:
            hours, minutes = elapsed_time(value[0], value[1])

            # Check results
            self.assertEqual(hours, value[2][0])
            self.assertEqual(minutes, value[2][1])

    def test__get_max_west_shadow_details__ok(self):
        building_list = [{"name": "Aticco", "apartments_count": 8, "distance": 1},
                         {"name": "01", "apartments_count": 4, "distance": 2},
                         {"name": "CEM", "apartments_count": 7, "distance": 1},
                         {"name": "30", "apartments_count": 1, "distance": -1}]

        # (<index>, [(<expected_max_west_shadow_index_floor_0>, <expected_max_west_shadow_distance_floor_0>)),
        #            (<expected_max_west_shadow_index_floor_1>, <expected_max_west_shadow_distance_floor_1>)),
        #               ...
        #            (<expected_max_west_shadow_index_floor_N>, <expected_max_west_shadow_distance_floor_N>))
        #           ]
        values = [
            (0, [(1, 1), (1, 1), (1, 1), (1, 1), (2, 3), (2, 3), (2, 3), (-1, 0)]),
            (1, [(2, 2), (2, 2), (2, 2), (2, 2)]),
            (2, [(3, 1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)]),
            (3, [(-1, 0)]),
        ]

        # Test main
        for value in values:

            # Assure that the values are coherent. There must be as many results per building as apartments (with one
            #  apartment per floor)
            self.assertEqual(len(value[1]), building_list[value[0]]["apartments_count"])

            for floor in range(building_list[value[0]]["apartments_count"]):
                max_west_shadow_index, max_west_shadow_distance = get_max_west_shadow_details(value[0], building_list,
                                                                                              floor)

                # Check results
                self.assertEqual(max_west_shadow_index, value[1][floor][0])
                self.assertEqual(max_west_shadow_distance, value[1][floor][1])

    def test__get_neighbourhood_sunlight_hours__ok(self):
        apartments_height = 1
        building_list = [{"name": "Aticco", "apartments_count": 8, "distance": 1},
                         {"name": "01", "apartments_count": 4, "distance": 2},
                         {"name": "CEM", "apartments_count": 7, "distance": 1},
                         {"name": "30", "apartments_count": 1, "distance": -1}]

        # Test main
        get_neighbourhood_sunlight_hours(building_list, DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"],
                                         DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"], apartments_height)

        # Check results
        expected_building_list = [
            {"name": "Aticco", "apartments_count": 8, "distance": 1,
             "dawn": ['08:14', '08:14', '08:14', '08:14', '08:14', '08:14', '08:14', '08:14'],
             "sunset": ['13:33', '13:46', '14:11', '15:08', '15:08', '15:42', '16:29', '17:25']
             },

            {"name": "01", "apartments_count": 4, "distance": 2,
             "dawn": ['12:27', '12:24', '12:20', '12:14'],
             "sunset": ['13:39', '13:46', '13:57', '14:11']
             },

            {"name": "CEM", "apartments_count": 7, "distance": 1,
             "dawn": ['12:27', '12:24', '12:20', '12:14', '12:06', '11:53', '11:28'],
             "sunset": ['15:08', '17:25', '17:25', '17:25', '17:25', '17:25', '17:25']
             },

            {"name": "30", "apartments_count": 1, "distance": -1,
             "dawn": ['12:27'],
             "sunset": ['17:25']
             }
        ]

        self.assertEqual(building_list, expected_building_list)
