
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound

#from ..account_manager import AccountManager

# For the sake of simplicity, in this test I will deactivate the CSRF protection for this test. In real production
# Cross Site Request Forgery Protection should be used.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class SunlightHoursView(View):
    """
        View that displays the balance of a user
    """

    def get(self, request):
        """
            Gets the number of sunlight hours of the specified apartment.

        :param request: HTTP request
        :return: HTTP response with the number of sunlight hours of the specified apartment (as specified in the Code
            Challenge)
        """
        #TODO retrieve apartment info from request

        #TODO CHECK that the apartment exists
        apartment = None  # DEBUGGING

        if apartment is None:
            # The apartment does not exists
            return HttpResponseNotFound("Unknown apartment")
        else:
            return HttpResponse(apartment.get_sunlight_hours_str())
