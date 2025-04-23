# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Person
from .serializers import PersonSerializer

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view

class PersonListView(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
def exchange_code_for_token(request):
    """Receives auth code from Angular and exchanges it for an access token."""
    code = request.data.get("code")
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    # Exchange code for tokens
    token_endpoint = settings.OIDC_CONFIG["TOKEN_ENDPOINT"]
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.OIDC_CONFIG["CLIENT_ID"],
        "client_secret": settings.OIDC_CONFIG.get("CLIENT_SECRET", ""),
        "code": code,
        "redirect_uri": settings.OIDC_CONFIG["REDIRECT_URI"],
    }

    response = requests.post(token_endpoint, data=data)
    if response.status_code != 200:
        return JsonResponse(response.json(), status=response.status_code)

    tokens = response.json()
    
    # Store token in Django session (or generate a custom JWT)
    return JsonResponse({
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
    })