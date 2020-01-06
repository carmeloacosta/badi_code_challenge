
import json
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

from ..controller import Controller

# For the sake of simplicity, in this test I will deactivate the CSRF protection for this test. In real production
# Cross Site Request Forgery Protection should be used.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class SunlightHoursView(View):
    """
        View that displays the balance of a user
    """

    @staticmethod
    def check_valid_body(body):
        """
            Checks that the input body contains the specified format. That is,

             - A neighbourhood name,
             - a building name,
             - and an apartment number (from 0 to N-1, lower to higher floor respectively).

        :return: (dict/None) The info of the properly specified body using the specified format; None otherwise.

            {
                "neighbourhood": <neighbourhood_name>,
                "building": <building_name>,
                "apartment": <apartment_number>
            }

            with:

                    <neighbourhood_name> : (str) Neighbourhood name (case sensitive)
                    <building_name> : (str) Building name (case sensitive)
                    <apartment> : (int) Apartment number (from 0 to N-1, lower to higher floor respectively).

        """
        result = None
        message = ""

        try:
            body = json.loads(body)
            result = {"neighbourhood": str(body["neighbourhood"]),
                      "building": str(body["building"]),
                      "apartment": int(body["apartment"])
                      }

        except json.decoder.JSONDecodeError:
            message = "Bad Body. It must be a JSON"

        except ValueError:
            message = "Bad Body. Apartment must be an integer value (from 0 to N-1) that specifies the floor"

        return result, message

    @staticmethod
    def get_sunlight_hours_str(apartment):
        """
            Returns the sunlight hours, as specified in the Code Challenge.

        :param apartment: (..models.Apartment) The information of the apartment to show sunlight hours string.
        :return: (str): The sunlight hours, following the format (the one specified in the Code Challenge):

                                <apartment_dawn> - <apartment_sunset>

                with
                        <apartment_dawn> : (str) The local time when starts the sunlight in the apartment. Follows the
                                            format:

                                                    HH:MM

                                    with
                                            HH: Hour   (from '00' to '23')
                                            MM: Minute (from '00' to '59')

                                    Examples: '08:14', '17:25'

                        <apartment_sunset> : (str) The local time when ends the sunlight in the apartment. Follows the
                                            same format as apartment_dawn.

        """
        return "{} - {}".format(apartment.dawn, apartment.sunset)

    def put(self, request):
        """
            Gets the number of sunlight hours of the specified apartment.

        :param request: HTTP request
        :return: HTTP response with the number of sunlight hours of the specified apartment (as specified in the Code
            Challenge)
        """
        request_info, message = SunlightHoursView.check_valid_body(request.body.decode())

        if request_info:
            if not Controller.is_running_db():
                message = "Service Unavailable."
                status = 503  # SERVICE UNAVAILABLE
                return HttpResponse(message, status=status)
            else:
                apartment = Controller.get_apartment_info(request_info)

                if apartment is None:
                    # The apartment does not exists
                    return HttpResponseNotFound("Unknown apartment.")
                else:
                    return HttpResponse(self.get_sunlight_hours_str(apartment))
        else:
            # Bad parameters
            return HttpResponseBadRequest(message)
