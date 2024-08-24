import ssl
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
import jwt

from auth.jwt_model import JWTToken

# Replace with your OIDC provider's details
ISSUER = "https://192.168.1.27:9090/realms/master"
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
CLIENT_ID = "test_clientid"
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{ISSUER}/protocol/openid-connect/auth",
    tokenUrl=f"{ISSUER}/protocol/openid-connect/token"
)

jwks_client = jwt.PyJWKClient(JWKS_URL, ssl_context=ssl._create_unverified_context())


async def verify_token(token: str = Depends(oauth2_scheme)) -> JWTToken:
    try:
        # Get the key id from the token header
        header = jwt.get_unverified_header(token)
        key = jwks_client.get_signing_key(header["kid"])

        # Decode and verify the token
        payload = jwt.decode(
            token,
            key.key,
            algorithms=["RS256"],
            audience="account",  # FIXME: should be clientid but the token has this
            issuer=ISSUER,
        )
        return JWTToken.model_validate(payload)
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=str(e))


async def can_edit(token: JWTToken = Depends(verify_token)) -> JWTToken:
    if not token.can_read():
        raise HTTPException(status_code=401, detail="You are not authorized to edit this resource") 
    return token


async def can_read(token: JWTToken = Depends(verify_token)) -> JWTToken:
    if not token.can_read():
        raise HTTPException(status_code=401, detail="You are not authorized to access this resource") 
    return token