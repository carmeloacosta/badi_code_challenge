#!/bin/python3

"""
    City module. Contains all information regarding with a full city
"""

from .constants import DEFAULT_CITY, DEFAULT_CITY_VALUES


class CityInitializationError(Exception):
    pass


class City():
    """
        Manages all the city information.
    """

    def __init__(self, city_info, name=DEFAULT_CITY, dawn=DEFAULT_CITY_VALUES[DEFAULT_CITY]["dawn"],
                 sunset=DEFAULT_CITY_VALUES[DEFAULT_CITY]["sunset"]):
        """
            Initializes the city with the specified info.

        :param city_info: (list of dict) List of neighbourhoods contained in the city (as described in the Code
            Challenge description)
        :param name: (str) Name of the city.
        :param dawn: (str) Dawn time. Local time at which starts the sunlight.
        :param sunset: (str) Sunset time. Local time at which ends the sunlight
        """
        # City name
        self.name = name
        # Dawn time. Local time at which starts the sunlight
        self.dawn = dawn
        # Sunset time. Local time at which ends the sunlight
        self.sunset = sunset

        # TODO. Initialize the whole city from city_info. Raises a CityInitializationError if something went wrong.

    def save(self):
        """
            Save city description to permanent storage.

        :return: None
        """
        #TODO
        pass
