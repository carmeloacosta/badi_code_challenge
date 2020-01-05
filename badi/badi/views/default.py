
from django.http import HttpResponse


def handler404(request, exception):
    status = 404
    message = "HTTP {}".format(status)
    return HttpResponse(message, status=status)


def handler500(request):
    status = 500
    message = "HTTP {}".format(status)
    return HttpResponse(message, status=status)
