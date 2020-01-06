#!/bin/python3


import os
from json import dumps
from django.test import TestCase

from ..settings import FIXTURE_DIRS
from ..city import City
from ..constants import DEFAULT_CITY, DEFAULT_CITY_VALUES
from ..controller import Controller


class CityTestCase(TestCase):

    maxDiff = None
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

        # FORMAT:
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

        # FORMAT:
        # [
        #     { neighborhood: <name_string>, apartments_height: <number>,
        #       buildings: [{name:<name_string>, apartments_count: <number>, distance: <number>,
        #                   dawn: [<floor_0_dawn>, <floor_1_dawn> ... <floor_N-1_dawn>],
        #                   sunset: [<floor_0_sunset>, <floor_1_sunset> ... <floor_N-1_sunset>]
        #                   }]
        #     }
        # ]
        expected_city_info = [
            {"neighborhood": "POBLENOU", "apartments_height": 1, "buildings":
                [{"name": "Aticco", "apartments_count": 8, "distance": 1,
                  "dawn": ["08:14", "08:14", "08:14", "08:14", "08:14", "08:14", "08:14", "08:14"],
                  "sunset": ["13:33", "13:46", "14:11", "15:08", "15:08", "15:42", "16:29", "17:25"]
                  },
                 {"name": "01", "apartments_count": 4, "distance": 2,
                  "dawn": ["12:27", "12:24", "12:20", "12:14"],
                  "sunset": ["13:39", "13:46", "13:57", "14:11"]
                  },
                 {"name": "CEM", "apartments_count": 7, "distance": 1,
                  "dawn": ["12:27", "12:24", "12:20", "12:14", "12:06", "11:53", "11:28"],
                  "sunset": ["15:08", "17:25", "17:25", "17:25", "17:25", "17:25", "17:25"]
                  },
                 {"name": "30", "apartments_count": 1, "distance": -1,
                  "dawn": ["12:27"],
                  "sunset": ["17:25"]
                  }
                 ]
             },
            {"neighborhood": "RAVAL", "apartments_height": 2, "buildings":
                [{"name": "Santa Monica", "apartments_count": 3, "distance": 1,
                  "dawn": ["08:14", "08:14", "08:14"],
                  "sunset": ["13:33", "14:11", "14:11"]
                  },
                 {"name": "La Capella", "apartments_count": 2, "distance": 1,
                  "dawn": ["12:20", "12:06"],
                  "sunset": ["13:12", "13:19"]
                  },
                 {"name": "CCCB", "apartments_count": 4, "distance": -1,
                  "dawn": ["12:20", "12:06", "11:28", "08:14"],
                  "sunset": ["17:25", "17:25", "17:25", "17:25"]
                  }
                 ]
             }
        ]

        # Test main
        new_city = City(city_info)

        # Check results
        self.assertEqual(new_city.name, DEFAULT_CITY)  # Default name
        self.assertEqual(new_city.dawn, DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"])  # Default dawn time
        self.assertEqual(new_city.sunset, DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"])  # Default sunset time
        self.assertEqual(new_city.info, expected_city_info)  # City info with per apartment sunlight info

    def test__city_save__ok(self):

        # FORMAT:
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

        # Test main
        new_city = City(city_info)
        new_city.save()

        # Check results

        # FORMAT:
        # [
        #     { neighborhood: <name_string>, apartments_height: <number>,
        #       buildings: [{name:<name_string>, apartments_count: <number>, distance: <number>,
        #                   dawn: [<floor_0_dawn>, <floor_1_dawn> ... <floor_N-1_dawn>],
        #                   sunset: [<floor_0_sunset>, <floor_1_sunset> ... <floor_N-1_sunset>]
        #                   }]
        #     }
        # ]
        expected_city_info = [
            {"neighbourhood": "POBLENOU", "apartments_height": 1, "buildings":
                [{"name": "Aticco", "apartments_count": 8, "distance": 1,
                  "dawn": ["08:14", "08:14", "08:14", "08:14", "08:14", "08:14", "08:14", "08:14"],
                  "sunset": ["13:33", "13:46", "14:11", "15:08", "15:08", "15:42", "16:29", "17:25"]
                  },
                 {"name": "01", "apartments_count": 4, "distance": 2,
                  "dawn": ["12:27", "12:24", "12:20", "12:14"],
                  "sunset": ["13:39", "13:46", "13:57", "14:11"]
                  },
                 {"name": "CEM", "apartments_count": 7, "distance": 1,
                  "dawn": ["12:27", "12:24", "12:20", "12:14", "12:06", "11:53", "11:28"],
                  "sunset": ["15:08", "17:25", "17:25", "17:25", "17:25", "17:25", "17:25"]
                  },
                 {"name": "30", "apartments_count": 1, "distance": -1,
                  "dawn": ["12:27"],
                  "sunset": ["17:25"]
                  }
                 ]
             },
            {"neighbourhood": "RAVAL", "apartments_height": 2, "buildings":
                [{"name": "Santa Monica", "apartments_count": 3, "distance": 1,
                  "dawn": ["08:14", "08:14", "08:14"],
                  "sunset": ["13:33", "14:11", "14:11"]
                  },
                 {"name": "La Capella", "apartments_count": 2, "distance": 1,
                  "dawn": ["12:20", "12:06"],
                  "sunset": ["13:12", "13:19"]
                  },
                 {"name": "CCCB", "apartments_count": 4, "distance": -1,
                  "dawn": ["12:20", "12:06", "11:28", "08:14"],
                  "sunset": ["17:25", "17:25", "17:25", "17:25"]
                  }
                 ]
             }
        ]

        for neighbourhood in expected_city_info:
            for building in neighbourhood["buildings"]:
                for floor in range(building["apartments_count"]):

                    apartment_info = {
                        "neighbourhood": neighbourhood["neighbourhood"],
                        "building": building["name"],
                        "apartment": floor
                    }

                    apartment = Controller.get_apartment_info(apartment_info)

                    self.assertEqual(apartment.building.neighbourhood.name, neighbourhood["neighbourhood"])
                    self.assertEqual(apartment.building.name, building["name"])
                    self.assertEqual(apartment.floor, floor)


