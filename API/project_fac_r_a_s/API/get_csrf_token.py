from django.middleware.csrf import get_token
from django.http import HttpResponse

def getTokenFunction(request):

    csrf_token = get_token(request)
    print(csrf_token)
    return HttpResponse(csrf_token)