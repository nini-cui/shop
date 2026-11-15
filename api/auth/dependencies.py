import jwt, os
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.deps import get_db
from sqlalchemy.orm import Session, joinedload
from schema import user

AUTHENTIK_ISSUER = os.environ["AUTHENTIK_ISSUER"]
JWKS_URL = os.environ["AUTHENTIK_JWKS_URL"]

bearer_scheme = HTTPBearer()
jwks_client = PyJWKClient(JWKS_URL)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    print("token is, ", token)
    
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=AUTHENTIK_ISSUER,
            options={
                "verify_aud": False,
            },
        )
        print("payload is: ", payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    # Get Authentik subject
    authentik_sub = payload.get("sub")

    if not authentik_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing subject",
        )

    # Retrieve user from our database
    user = (
        db.query(user.User)
        .options(
            joinedload(user.User.user_roles).joinedload(user.UserRole.role)
        )
        .filter(user.User.authentik_sub == authentik_sub)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not registered in this application",
        )

    for user_role in user.user_roles:
        print("user role is: ", user_role.role.name)

    return user
