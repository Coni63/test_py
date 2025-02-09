from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        scopes = self.get_settings("OIDC_RP_SCOPES", "openid")
        return "openid" in scopes.split()