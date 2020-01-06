
# Add logger
import logging
logger = logging.getLogger(__name__) #TODO: Replace logger with Dependency Injected global logger

from .constants import DEFAULT_CITY
from .models import Apartment, Building, Neighbourhood, City


class Controller():
    """
        Implements the Car Pooling bussiness logic. It access the underlying data base system in order to persist the
        required data.
    """

    @staticmethod
    def is_running_db():
        """
            Tells if the underlying data base system is up and running

        :return: (bool) True if the underlying data base system is up and running; False otherwise.
        """
        result = False
        try:
            #
            # NOTE: Check here any condition that could turn temporary unavailable the DB
            #
            aqs = Apartment.objects.filter(id=1)
            bqs = Building.objects.filter(id=1)
            nqs = Neighbourhood.objects.filter(id=1)
            cqs = City.objects.filter(id=1)

            if len(aqs) > 1 or len(bqs) > 1 or len(nqs) > 1 or len(cqs) > 1:
                # Force real execution of lazy querysets (and enforce data consistency)
                logger.exception("Data inconsistency detected - The DB is in an uncertain state. Check it out")
                raise Exception("Inconsistent Data")

            result = True

        except Exception as e:
            # If anything wrong happens, assume the underlying data base system is not available right now.
            logger.exception("While trying to check DB activity: {}".format(e))

        return result

    @staticmethod
    def get_apartment_info(apartment_info):
        """
            Retrieves the information of the specified apartment.

        :param apartment_info: (dict)
        :return:
        """
        try:
            try:
                cqs = City.objects.filter(name=apartment_info["city"])
            except KeyError:
                # Use default city
                cqs = City.objects.filter(name=DEFAULT_CITY)

            nqs = Neighbourhood.objects.filter(city=cqs[0]).filter(name=apartment_info["neighbourhood"])
            bqs = Building.objects.filter(name=apartment_info["building"]).filter(neighbourhood=nqs[0])
            aqs = Apartment.objects.filter(building=bqs[0]).filter(floor=apartment_info["floor"])

            return aqs[0]

        except KeyError:
            result = None

        return result

