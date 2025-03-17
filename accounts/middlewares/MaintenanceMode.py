from django.conf import settings
from django.http import HttpResponse

class MaintenanceModeMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if settings.MAINTENANCE_MODE:
            return HttpResponse("Service is under maintenance.", status=503)
        return self.get_response(request)