from django.http import JsonResponse

class ExceptionHandlingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        try:
            response = self.get_response(request)
        except Exception as e:
            response  = JsonResponse({
                'error':'An unexpected error occurred.',
                'details':str(e)
            },status = 500)
        return response