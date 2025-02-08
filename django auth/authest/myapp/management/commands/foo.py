from django.core.management.base import BaseCommand, CommandError
import requests


class Command(BaseCommand):
    help = "Test"

    def handle(self, *args, **options):
        token = self.get_keycloak_token(
            base_url='http://pi5:8080',
            client_id='my-backend-app',
            client_secret='dKBGsoVz9ER5U4GGGk3MXoqpFHohYIpM',
            username='testuser',
            password='password'
        )
        print(token)

        access_token = token['access_token']
        print("\n", access_token, "\n")

        introspection_response = self.introspect_token(
            base_url='http://pi5:8080',
            client_id='my-backend-app',
            client_secret='dKBGsoVz9ER5U4GGGk3MXoqpFHohYIpM',
            token=access_token
        )
        print(introspection_response)

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
    
    def introspect_token(self, base_url, client_id, client_secret, token):
        """
        Introspect a token to check its validity and get additional information.
        
        Args:
            base_url (str): Base URL of the Keycloak server
            client_id (str): Client ID of the application
            client_secret (str): Client secret of the application
            token (str): The access token to introspect
            
        Returns:
            dict: The response JSON containing the token information
        """
        introspect_url = f"{base_url}/realms/master/protocol/openid-connect/token/introspect"
        
        # Prepare the request data
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'token': token
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Make the request
        response = requests.post(introspect_url, data=payload, headers=headers)
        
        # Check if request was successful
        response.raise_for_status()
        
        return response.json()
