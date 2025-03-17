from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        ip = request.META.get('REMOTE_ADDR')
        key = f"rate_limit_{ip}"
        limit = 100
        current = cache.get(key,0)

        if current >= limit:
            return HttpResponseForbidden("Rate limit exceeded.")
        
        cache.set(key,current + 1,60)
        return self.get_response(request)
