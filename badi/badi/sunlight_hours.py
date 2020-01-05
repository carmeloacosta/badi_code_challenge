#!/bin/python3

"""
    Module that gathers tools to compute sunlight hours.
"""


def get_apartment_dawn(angle, city_dawn, city_sunset):
    """
        Returns the local time when starts the sunlight in the apartment.

    :param angle: (float) The angle of the shadow (and the soil) of the tallest building on the east (in grades).
    :param city_dawn: (str) The local time when starts the sunlight in the city. Follows the format:

                                            HH:MM
                with
                        HH: Hour   (from '00' to '23')
                        MM: Minute (from '00' to '59')

                Examples: '08:14', '17:25'

    :param city_sunset: (str) The local time when ends the sunlight in the city. Follows the same format as city_dawn.
    :return: (str) The local time when starts the sunlight in the apartment. Follows the same format as city_dawn.
    """
    pass
