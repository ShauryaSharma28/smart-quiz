# smartquiz/middleware.py
from django.utils.deprecation import MiddlewareMixin

class NoCacheAuthPages(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/accounts/'):
            response['Cache-Control'] = 'no-store'
        return response
