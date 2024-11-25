import re

from django.http import JsonResponse


class UUIDValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/v1/wallets/'):
            match = re.match(r'/api/v1/wallets/([a-f0-9\-]{36})/',
                             request.path)
            if not match:
                return JsonResponse(
                    {'error': 'Неверный формат UUID'},
                    status=400
                )

        response = self.get_response(request)
        return response
