#!/bin/python3

"""
    Data models
"""

from django.db import models


class City(models.Model):
    """
        City Entity. There will be a row in this table for each city.

        NOTE: Although the Code Challenge assumes only Barcelona, it is quite easy to design it to accept any number of
        cities.
    """
    name = models.CharField(max_length=128, primary_key=True)
    # The time when the sunlight starts in this city
    dawn = models.CharField(max_length=5)
    # The time when the sunlight ends in this city
    sunset = models.CharField(max_length=5)

    def __str__(self):

        return "< name={}, dawn={}, sunset={} >".format(self.name, self.dawn, self.sunset)


class Neighbourhood(models.Model):
    """
        Neighbourhood Entity. There will be a row in this table for each neighbourhood.
    """
    id = models.IntegerField(primary_key=True)
    # Neighbourhood name
    name = models.CharField(max_length=128)
    # The height of the apartments in this neighbourhood
    apartments_height = models.IntegerField()
    # The city in which is located this neighbourhood
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):

        return "< id={}, name={}, apartments_height={}, city={} >".format(self.id, self.name, self.apartments_height,
                                                                          self.city.name)


class Building(models.Model):
    """
        Building Entity. There will be a row in this table for each building.
    """
    id = models.IntegerField(primary_key=True)
    # Building name
    name = models.CharField(max_length=128)
    # The total number of floors
    floors = models.IntegerField()
    # The neighbourhood in which is located this building
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    # Position that occupies this building from East to West (from 0 to N-1)
    east_position = models.IntegerField()
    # Distance to the prior building in the same Neighbourhood. -1 means that this is the first from the East.
    prev_distance = models.IntegerField()
    # Distance to the next building in the same Neighbourhood. -1 means that this is the last from the East.
    next_distance = models.IntegerField()

    def __str__(self):

        return "< id={}, name={}, floors={}, neighbourhood={}, east_position={}, prev_distance={}, next_distance={} " \
               ">".format(self.id, self.name, self.floors, self.neighbourhood.name, self.east_position,
                          self.prev_distance, self.next_distance)


class Apartment(models.Model):
    """
        Apartment Entity. There will be a row in this table for each apartment.
    """
    id = models.IntegerField(primary_key=True)
    # The building where is located
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    # The building floor that occupies (from 0 to N-1)
    floor = models.IntegerField()
    # The time when the sunlight starts in this apartment
    dawn = models.CharField(max_length=5)
    # The time when the sunlight ends in this apartment
    sunset = models.CharField(max_length=5)

    def __str__(self):

        return "< id={}, building={}, floor={}, dawn={}, sunset={} >".format(self.id, self.building.name, self.floor,
                                                                             self.dawn, self.sunset)
