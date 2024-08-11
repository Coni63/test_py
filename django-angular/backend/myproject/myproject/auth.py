import jwt
from jwt import InvalidTokenError
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings

# class KeycloakBackend(BaseBackend):
#     def authenticate(self, request, token=None):
#         print("kjlhgdq")
#         if token is None:
#             return None
        
#         try:
#             # Decode the JWT token using the public key from Keycloak
#             decoded_token = jwt.decode(
#                 token,
#                 settings.KEYCLOAK_PUBLIC_KEY,   # This should be your Keycloak public key
#                 algorithms=["RS256"],
#                 audience=settings.KEYCLOAK_CLIENT_ID,  # Your Keycloak client ID
#             )
            
#             print(decoded_token)

#             username = decoded_token.get("preferred_username", None)
#             if not username:
#                 return None
            
#             # Get or create the user based on the username
#             user, created = User.objects.get_or_create(username=username)
            
#             return user
            
#         except (InvalidTokenError, InvalidToken):
#             return None
    
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

class KeycloakJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        # Step 1: Extract the Authorization header
        header = self.get_header(request)
        if header is None:
            print("No Authorization header found.")
            return None

        # Step 2: Extract the Bearer token from the header
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            print("No Bearer token found in the Authorization header.")
            return None

        print("Raw token:", raw_token)

        try:
            # Step 3: Decode and validate the JWT token using the Keycloak public key
            decoded_token = jwt.decode(
                raw_token,
                settings.KEYCLOAK_PUBLIC_KEY,   # Your Keycloak public key
                algorithms=["RS256"],
                audience=[settings.KEYCLOAK_CLIENT_ID, 'account'],  # Your Keycloak client ID
            )
            print("Token decoded successfully:", decoded_token)

            # Step 4: Validate and extract user information from the token
            # validated_token = self.get_validated_token(decoded_token)

            print("validated_token")
            user = self.get_user(decoded_token)
            return user, decoded_token

        except InvalidTokenError as e:
            print(f"Token validation error: {e}")
            return None

    def get_user(self, validated_token):
        """
        Get or create a Django user based on the validated JWT token.
        """
        username = validated_token.get("preferred_username")
        email = validated_token.get("email", "")
        first_name = validated_token.get("given_name", "")
        last_name = validated_token.get("family_name", "")

        if not username:
            raise InvalidToken("Token contained no recognizable username")

        # Get or create the user in Django's local database
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
        )

        if not created:
            # Optionally, update user information if already exists
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        return user