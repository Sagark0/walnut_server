from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return HttpResponse("Backend is running")
