#!/bin/python3

"""
    Module that gathers tools to compute sunlight hours.
"""


def get_apartment_dawn(angle, city_seconds_per_grade, city_dawn):
    """
        Returns the local time when starts the sunlight in the apartment.

    :param angle: (float) The angle of the shadow (and the soil) of the tallest building on the east (in grades).
    :param city_seconds_per_grade: (float) The number of elapsed seconds for each unitary increment in the angle that
        between the sunlight and the soil.

        RECALL that, following the Code Challenge definition, the total number of seconds elapsed from the city dawn
        to the city sunset are equally distributed between the 180 grades that cover the full dawn-sunset range.

    :param city_dawn: (str) The local time when starts the sunlight in the apartment. Follows the format:

                                            HH:MM
                with
                        HH: Hour   (from '00' to '23')
                        MM: Minute (from '00' to '59')

                Examples: '08:14', '17:25'

    :return: (str) The local time when starts the sunlight in the apartment. Follows the same format than city_dawn.
    """
    elapsed_seconds_from_dawn = int(angle * city_seconds_per_grade)
    elapsed_hours_from_dawn = 0
    elapsed_minutes_from_dawn = int(elapsed_seconds_from_dawn/60)

    if elapsed_minutes_from_dawn > 59:
        elapsed_hours_from_dawn = int(elapsed_minutes_from_dawn/60)
        elapsed_minutes_from_dawn -= elapsed_hours_from_dawn * 60

    city_dawn_hour_int = int(city_dawn.split(':')[0])
    city_dawn_minute_int = int(city_dawn.split(':')[1])

    apartment_dawn_hour_int = city_dawn_hour_int + elapsed_hours_from_dawn
    apartment_dawn_minute_int = city_dawn_minute_int + elapsed_minutes_from_dawn

    if apartment_dawn_minute_int > 59:
        apartment_dawn_minute_int = 60 - apartment_dawn_minute_int
        apartment_dawn_hour_int += 1

    result = "{}:{}".format(str(apartment_dawn_hour_int).rjust(2, '0'), apartment_dawn_minute_int)

    return result


def get_apartment_sunset(angle, city_seconds_per_grade, city_sunset):
    """
        Returns the local time when ends the sunlight in the apartment.

    :param angle: (float) The angle of the shadow (and the soil) of the tallest building on the west (in grades).
    :param city_seconds_per_grade: (float) The number of elapsed seconds for each unitary increment in the angle that
        between the sunlight and the soil.

        RECALL that, following the Code Challenge definition, the total number of seconds elapsed from the city dawn
        to the city sunset are equally distributed between the 180 grades that cover the full dawn-sunset range.

    :param city_sunset: (str) The local time when starts the sunlight in the apartment. Follows the format:

                                            HH:MM
                with
                        HH: Hour   (from '00' to '23')
                        MM: Minute (from '00' to '59')

                Examples: '08:14', '17:25'

    :return: (str) The local time when starts the sunlight in the apartment. Follows the same format than city_sunset.
    """
    elapsed_seconds_from_dawn = int(angle * city_seconds_per_grade)
    elapsed_hours_from_dawn = 0
    elapsed_minutes_from_dawn = int(elapsed_seconds_from_dawn/60)

    if elapsed_minutes_from_dawn > 59:
        elapsed_hours_from_dawn = int(elapsed_minutes_from_dawn/60)
        elapsed_minutes_from_dawn -= elapsed_hours_from_dawn * 60

    city_dawn_hour_int = int(city_sunset.split(':')[0])
    city_dawn_minute_int = int(city_sunset.split(':')[1])

    apartment_dawn_hour_int = city_dawn_hour_int - elapsed_hours_from_dawn
    apartment_dawn_minute_int = city_dawn_minute_int - elapsed_minutes_from_dawn

    if apartment_dawn_minute_int < 0:
        apartment_dawn_minute_int = 60 + apartment_dawn_minute_int
        apartment_dawn_hour_int -= 1

    result = "{}:{}".format(str(apartment_dawn_hour_int).rjust(2, '0'), apartment_dawn_minute_int)

    return result
