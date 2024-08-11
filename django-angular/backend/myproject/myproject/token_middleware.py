from django.utils.deprecation import MiddlewareMixin

class KeycloakMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.headers.get('Authorization', None)
        if auth is not None:
            token_type, token = auth.split()
            if token_type.lower() == 'bearer':
                request.token = token
        return None