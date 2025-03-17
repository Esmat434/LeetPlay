class ScurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response["X-Content-Type-Options"] = "nosniff"

        response["X-Frame-Options"] = "DENY"

        response["X-XSS-Protection"] = "1; mode=block"

        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
