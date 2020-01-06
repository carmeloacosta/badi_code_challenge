#!/bin/python3

"""
    Module that gathers tools to compute sunlight hours.
"""

from math import atan, degrees


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

    :return: (str) The local time when starts the sunlight in the apartment. Follows the same format as city_dawn.
    """
    elapsed_seconds_from_dawn = int(angle * city_seconds_per_grade)
    elapsed_hours_from_dawn = 0
    elapsed_minutes_from_dawn = int(elapsed_seconds_from_dawn/60)

    while elapsed_minutes_from_dawn > 59:
        elapsed_hours_from_dawn = int(elapsed_minutes_from_dawn/60)
        elapsed_minutes_from_dawn -= elapsed_hours_from_dawn * 60

    city_dawn_hour_int = int(city_dawn.split(':')[0])
    city_dawn_minute_int = int(city_dawn.split(':')[1])

    apartment_dawn_hour_int = city_dawn_hour_int + elapsed_hours_from_dawn
    apartment_dawn_minute_int = city_dawn_minute_int + elapsed_minutes_from_dawn

    while apartment_dawn_minute_int > 59:
        apartment_dawn_minute_int = apartment_dawn_minute_int - 60
        apartment_dawn_hour_int += 1

    result = "{}:{}".format(str(apartment_dawn_hour_int).rjust(2, '0'), str(apartment_dawn_minute_int).rjust(2, '0'))

    return result


def get_apartment_sunset(angle, city_seconds_per_grade, city_sunset):
    """
        Returns the local time when ends the sunlight in the apartment.

    :param angle: (float) The angle of the shadow (and the soil) of the tallest building on the west (in grades).
    :param city_seconds_per_grade: (float) The number of elapsed seconds for each unitary increment in the angle that
        between the sunlight and the soil.

        RECALL that, following the Code Challenge definition, the total number of seconds elapsed from the city dawn
        to the city sunset are equally distributed between the 180 grades that cover the full dawn-sunset range.

    :param city_sunset: (str) The local time when ends the sunlight in the apartment. Follows the format:

                                            HH:MM
                with
                        HH: Hour   (from '00' to '23')
                        MM: Minute (from '00' to '59')

                Examples: '08:14', '17:25'

    :return: (str) The local time when starts the sunlight in the apartment. Follows the same format as city_sunset.
    """
    remaining_seconds_until_sunset = int(angle * city_seconds_per_grade)
    remaining_hours_until_sunset = 0
    remaining_minutes_until_sunset = int(remaining_seconds_until_sunset/60)

    while remaining_minutes_until_sunset > 59:
        remaining_hours_until_sunset = int(remaining_minutes_until_sunset/60)
        remaining_minutes_until_sunset -= remaining_hours_until_sunset * 60

    city_sunset_hour_int = int(city_sunset.split(':')[0])
    city_sunset_minute_int = int(city_sunset.split(':')[1])

    apartment_sunset_hour_int = city_sunset_hour_int - remaining_hours_until_sunset
    apartment_sunset_minute_int = city_sunset_minute_int - remaining_minutes_until_sunset

    while apartment_sunset_minute_int < 0:
        apartment_sunset_minute_int = apartment_sunset_minute_int + 60
        apartment_sunset_hour_int -= 1

    result = "{}:{}".format(str(apartment_sunset_hour_int).rjust(2, '0'),
                            str(apartment_sunset_minute_int).rjust(2, '0'))

    return result


def elapsed_time(start_time, end_time):
    """
        Returns the time elapsed in the interval comprised between start_time and end_time.

    :param start_time: (str) The start time of the interval. Follows the format:

                                            HH:MM
                with
                        HH: Hour   (from '00' to '23')
                        MM: Minute (from '00' to '59')

                Examples: '08:14', '17:25'
    :param end_time: (str) The end time of the interval. Follows the same format as start_time.
    :return: (tuple) Follows the format:

                                    <hours>, <minutes>
                with
                        <hours>: (int) Number of hours elapsed
                        <minutes>: (int) Number of minutes elapsed
    """
    start_time_hour_int = int(start_time.split(':')[0])
    start_time_minute_int = int(start_time.split(':')[1])

    end_time_hour_int = int(end_time.split(':')[0])
    end_time_minute_int = int(end_time.split(':')[1])

    elapsed_minutes = end_time_minute_int - start_time_minute_int
    elapsed_hours = end_time_hour_int - start_time_hour_int

    if elapsed_minutes < 0:
        elapsed_minutes += 60
        elapsed_hours -= 1

    return elapsed_hours, elapsed_minutes


def get_max_west_shadow_details(index, building_list, floor):
    """
        Given a building and a list of buildings, returns the position of the building on the west of the specified one,
        that creates the highest shadow from the west (i.e., from overhead to sunset position of the Sun).

        IMPLEMENTATION NOTE: Since this function does not return angles, and the inner usage of angles is restricted to
        angle comparison, I will simplify angle = atan(angle), since both have the same comparison (performance reason).

    :param index: (int) Position of the building in the list of buildings (0 to N-1).
    :param building_list: (list of dict) Follows the same format as the field "buildings" within each
        neighbourhood specified in the init API endpoint described in the Code Challenge. That is:

            [{name:<name_string>, apartments_count: <number>, distance: <number>}]

            As specified in the Code Challenge, it is assumed that the building list is ordered from east to west.

    :param index: (int) Floor of the building to make the measurement from (0 to N-1).

            NOTICE that depending on the floor height it could be a different object the one that projects its shadow
            on it.

    :return: (tuple) Following the format:

                    (<max_west_shadow_index>, <max_west_shadow_distance>)

                with:

                    <max_west_shadow_index> : (int) Position of the building that creates the highest shadow on the
                        west in the list of buildings (0 to N-1).
                    <max_west_shadow_distance> : (int) Distance between the specified building and the building that
                        creates the highest shadow on the west.

    """
    # Maximum shadow angle from the obstacles on the west.
    max_west_shadow_angle = 0
    # Distance to the the building that creates the maximum shadow angle on the west.
    max_west_shadow_distance = 0
    # Accumulated distance from the first building on the west
    acc_west_distance = 0
    # Index to the building that creates the maximum shadow angle on the west.
    max_west_shadow_index = -1

    for w_index in range(index, len(building_list)-1):
        # Update distance
        acc_west_distance += building_list[w_index]["distance"]
        if building_list[w_index+1]["apartments_count"] - (floor + 1) >= 0:
            #
            # As the relative position is higher the perspective changes
            #
            angle = float(building_list[w_index+1]["apartments_count"] - (floor - 1)) / float(acc_west_distance)
            if angle > max_west_shadow_angle:
                max_west_shadow_angle = angle
                max_west_shadow_index = w_index + 1
                max_west_shadow_distance = acc_west_distance

    if max_west_shadow_index == -1 and max_west_shadow_distance == 0:
        # Mark "no distance" or "infinite distance" as index -1
        max_west_shadow_index = -1
        max_west_shadow_distance = 0

    return max_west_shadow_index, max_west_shadow_distance


def get_neighbourhood_sunlight_hours(building_list, city_dawn, city_sunset, apartment_height):
    """
        Adds per apartment dawn and sunset info to the specified neighbourhood. That is, for each building in the
        neighbourhood two new lists will be added, dawn and sunset, that specify the time when the sunlight starts and
        ends for each apartment. These lists will be sorted from the lowest to the highest floor within each building.

        ASSUMPTION: Since the Code Challenge it is not clear enough regarding the distribution of each neighbourhood
        regarding to other neighbourhoods, I assume that each neighbourhood has no obstacles neither at the east nor
        the west. That is, I assume that the first building of each neighbourhood has infinite distance to the next
        obstacle (that could reduce the amount of sunlight) on the east. The same is assumed for the last building of
        each neighbourhood on the west.

    :param building_list: (list of dict) Follows the same format as the field "buildings" within each
        neighbourhood specified in the init API endpoint described in the Code Challenge. That is:

            [{name:<name_string>, apartments_count: <number>, distance: <number>}]

            As specified in the Code Challenge, it is assumed that the building list is ordered from east to west.

    :param city_dawn: (str) The local time when starts the sunlight in the city. Follows the format:

                                            HH:MM
                with
                        HH: Hour   (from '00' to '23')
                        MM: Minute (from '00' to '59')

                Examples: '08:14', '17:25'

    :param city_sunset: (str) The local time when ends the sunlight in the city. Follows the same format as city_dawn.
    :param apartment_height: (int) The height of the apartments.
    :return: None
    """
    # Compute the number of elapsed seconds for each grade of the sunlight, assuming (as said in the Code Challenge)
    # that the sun rises in the east and travels at a constant radial speed until setting
    city_sunlight_hours, city_sunlight_minutes = elapsed_time(city_dawn, city_sunset)

    city_sunlight_seconds = city_sunlight_hours * 3600 + city_sunlight_minutes * 60
    city_seconds_per_grade = float(city_sunlight_seconds)/float(180)

    # Maximum shadow angle from the obstacles on the east.
    max_east_shadow_angle = 0
    # Distance to the the building that creates the maximum shadow angle on the east.
    max_east_shadow_distance = 0
    # Accumulated distance from the first building on the east
    acc_east_distance = 0
    # Index to the building that creates the maximum shadow angle on the east.
    max_east_shadow_index = -1

    for index, building in enumerate(building_list):
        dawn = []
        sunset = []

        for floor in range(building["apartments_count"]):

            #
            # EAST SIDE
            #

            # Get angle of the highest shadow on the east. Notice that the higher the floor the lower the shadow from
            # other obstacles.
            try:
                angle = degrees(atan(((float(building_list[max_east_shadow_index]["apartments_count"]) -
                                      float(floor))*apartment_height)/float(max_east_shadow_distance)))

            except (ZeroDivisionError, IndexError):
                # The first building has no obstacles on the east
                angle = 0

            dawn.append(get_apartment_dawn(angle, city_seconds_per_grade, city_dawn))

            #
            # WEST SIDE
            #

            max_west_shadow_index, max_west_shadow_distance = get_max_west_shadow_details(index, building_list, floor)

            # Get angle of the highest shadow on the west. Notice that the higher the floor the lower the shadow from
            # other obstacles.
            try:
                angle = degrees(atan(((float(building_list[max_west_shadow_index]["apartments_count"]) -
                                      float(floor))*apartment_height)/float(max_west_shadow_distance)))

            except (ZeroDivisionError, IndexError):
                # The last building has no obstacles on the west
                angle = 0

            sunset.append(get_apartment_sunset(angle, city_seconds_per_grade, city_sunset))

        # Update building info
        building["dawn"] = dawn
        building["sunset"] = sunset

        # Update distance
        acc_east_distance += building["distance"]

        # Before proceeding with the next building on the west, update the max east shadow with the current building
        # (if proceeds)
        angle = float(building["apartments_count"]) / float(building["distance"])
        if angle > max_east_shadow_angle:
            max_east_shadow_angle = angle
            max_east_shadow_index = index
            max_east_shadow_distance = acc_east_distance


def compute_city_sunlight_hours(city_info, city_dawn, city_sunset):
    """
        Given the info of a city updates this info computing, for each apartment, both the dawn and sunset hour. That
        is, it is computed both the time the sunlight starts and the time the sunlight ends for each apartment of the
        city.

        [{ neighborhood: <name_string>, apartments_height: <number>, buildings: [{name:
        <name_string>, apartments_count: <number>, distance: <number>}]}]

    :param city_info: (list of dicts) City info (as described in the Code Challenge). Therefore, the expected format
        is as follows:

        [
            { neighborhood: <name_string>, apartments_height: <number>,
              buildings: [{name:<name_string>, apartments_count: <number>, distance: <number>}]
            }
        ]

        IMPORTANT: THIS IS AN INPUT/OUTPUT PARAMETER
            The city_info must be modified to add, for each building, two new lists, dawn and sunset, that specify the
            apartment dawn time and sunset time for each floor (sorted from 0 to N-1 floor).

            The resulting format is as follows:

        [
            { neighborhood: <name_string>, apartments_height: <number>,
              buildings: [{name:<name_string>, apartments_count: <number>, distance: <number>,
                          dawn: [<floor_0_dawn>, <floor_1_dawn> ... <floor_N-1_dawn>],
                          sunset: [<floor_0_sunset>, <floor_1_sunset> ... <floor_N-1_sunset>]
                          }]
            }
        ]

            with:
                    <floor_N_dawn> and <floor_N_sunset> following the format

                                                        HH:MM
                            with
                                    HH: Hour   (from '00' to '23')
                                    MM: Minute (from '00' to '59')

                            Examples: '08:14', '17:25'

    :param city_dawn: (str) The local time when starts the sunlight in the city. Follows the format:

                                            HH:MM
                with
                        HH: Hour   (from '00' to '23')
                        MM: Minute (from '00' to '59')

                Examples: '08:14', '17:25'

    :param city_sunset: (str) The local time when ends the sunlight in the city. Follows the same format as city_dawn.
    :return: (bool) True is successfully computed; False otherwise.
    """
    result = True

    try:
        for neighbourhood in city_info:
            get_neighbourhood_sunlight_hours(neighbourhood["buildings"], city_dawn, city_sunset,
                                             neighbourhood["apartments_height"])

    except (TypeError, KeyError):
        result = False

    return result
