import json

from django.views import View
from django.http import HttpResponse

from ..city import City, CityInitializationError

# For the sake of simplicity, in this test I will deactivate the CSRF protection for this test. In real production
# Cross Site Request Forgery Protection should be used.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class InitView(View):
    """
        View that displays the initialization of a city
    """
    def post(self, request):
        """
            Initializes a city with the values received in the string JSON contained in the body (as described in the
            Code Challenge description).

        :param request: HTTP request
        :return: HTTP response
        """
        result = True
        try:
            body = json.loads(request.body)

            try:
                new_city = City(body)
                new_city.save()
                message = "{} city updated".format(new_city.name)

            except CityInitializationError:
                result = False
                message = "Invalid city description"

        except json.decoder.JSONDecodeError:
            result = False
            message = "Bad Body. It must be a JSON"

        status = 200
        if not result:
            status = 400

        return HttpResponse(message, status=status)
