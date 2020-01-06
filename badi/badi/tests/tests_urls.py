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

        # Test main
        response = self.client.post('/init',
                                    dumps(body),
                                    content_type="application/json")

        # Check results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Barcelona city updated")

    def test__init__ok(self):

        body = [
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
        response = self.client.post('/init',
                                    dumps(body),
                                    content_type="application/json")

        # Check results
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Barcelona city updated")

    def test__get_sunlight_hours__ok(self):

        body = [
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

        # IMPLEMENTATION NOTE: This should be done using fixtures, instead of an init call. I will use it just to save
        #  up a little Code Challenge development time (simplify). In a real product, it should be done using fixtures.

        # Initialize data base
        response = self.client.post('/init',
                                    dumps(body),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 200)

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
        for neighbourhood in expected_city_info:
            for building in neighbourhood["buildings"]:
                for floor in range(building["apartments_count"]):

                    body = {
                        "neighbourhood": neighbourhood["neighborhood"],
                        "building": building["name"],
                        "apartment": floor
                    }

                    response = self.client.put('/getSunlightHours',
                                                dumps(body),
                                                content_type="application/json")

                    # Check results
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.content.decode(), "{} - {}".format(building["dawn"][floor],
                                                                                 building["sunset"][floor]))
