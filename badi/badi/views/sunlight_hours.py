
import json
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest


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

    def put(self, request):
        """
            Gets the number of sunlight hours of the specified apartment.

        :param request: HTTP request
        :return: HTTP response with the number of sunlight hours of the specified apartment (as specified in the Code
            Challenge)
        """
        request_info, message = SunlightHoursView.check_valid_body(request.body.decode())

        if request_info:
            #TODO CHECK that the apartment exists
            apartment = None  # DEBUGGING Apartment(request_info)

            if apartment is None:
                # The apartment does not exists
                return HttpResponseNotFound("Unknown apartment")
            else:
                return HttpResponse(apartment.get_sunlight_hours_str())
        else:
            # Bad parameters
            return HttpResponseBadRequest(message)
