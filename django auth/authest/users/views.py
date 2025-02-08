# ===============>>>> DRAFT <<<<<<<<<<<<<==============================


from django.shortcuts import render

# Create your views here.
# views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class KeycloakTokenView(APIView):
    def post(self, request):
        base_url = "http://pi5:8080"  # Or fetch from settings
        client_id = "my-backend-app"
        client_secret = "dKBGsoVz9ER5U4GGGk3MXoqpFHohYIpM"
        username = request.data.get("username")
        password = request.data.get("password")
        
        try:
            token_data = self.get_keycloak_token(
                base_url, client_id, client_secret, username, password
            )
            return Response(token_data)
        except requests.exceptions.HTTPError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Your existing helper method
    def get_keycloak_token(self, base_url, client_id, client_secret, username, password):
        """
        Get an access token from Keycloak using password grant type.
        
        Args:
            base_url (str): Base URL of the Keycloak server
            client_id (str): Client ID of the application
            client_secret (str): Client secret of the application
            username (str): Username of the user
            password (str): Password of the user
            
        Returns:
            dict: The response JSON containing the access token and other details
        """
        token_url = f"{base_url}/realms/master/protocol/openid-connect/token"
        
        # Prepare the request data
        payload = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Make the request
        response = requests.post(token_url, data=payload, headers=headers)
        
        # Check if request was successful
        response.raise_for_status()
        
        return response.json()


class KeycloakRefreshView(APIView):
    def post(self, request):
        base_url = "http://pi5:8080"
        client_id = "my-backend-app"
        client_secret = "dKBGsoVz9ER5U4GGGk3MXoqpFHohYIpM"
        refresh_token = request.data.get("refresh_token")
        
        token_url = f"{base_url}/realms/master/protocol/openid-connect/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
        
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({"error": "Refresh failed"}, status=status.HTTP_400_BAD_REQUEST)
        

class KeycloakLogoutView(APIView):
    def post(self, request):
        base_url = "http://pi5:8080"
        client_id = "my-backend-app"
        client_secret = "dKBGsoVz9ER5U4GGGk3MXoqpFHohYIpM"
        refresh_token = request.data.get("refresh_token")
        
        logout_url = f"{base_url}/realms/master/protocol/openid-connect/logout"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
        
        response = requests.post(logout_url, data=payload)
        if response.status_code == 204:
            return Response({"message": "Logged out"})
        else:
            return Response({"error": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST)
        


# urls.py
from django.urls import path
from .views import KeycloakTokenView, KeycloakRefreshView, KeycloakLogoutView

urlpatterns = [
    path('api/login/', KeycloakTokenView.as_view(), name='keycloak-login'),
    path('api/refresh/', KeycloakRefreshView.as_view(), name='keycloak-refresh'),
    path('api/logout/', KeycloakLogoutView.as_view(), name='keycloak-logout'),
]