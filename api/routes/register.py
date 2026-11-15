from fastapi import APIRouter, Depends, HTTPException, status
from db import deps
from auth import dependencies
from sqlalchemy.orm import Session
from schema import user

router = APIRouter(prefix="/register", tags=["Register"])


@router.post("/")
def register_buyer(
    payload: dict = Depends(dependencies.verify_token),
    db: Session = Depends(deps.get_db),
):
    authentik_sub = payload.get("sub")
    email = payload.get("email")

    # Validate required token claims
    if not authentik_sub or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing required user information",
        )

    # Check whether user already exists
    current_user = (
        db.query(user.User).filter(user.User.authentik_sub == authentik_sub).first()
    )

    if current_user:
        return current_user

    # Find default buyer role
    buyer_role = db.query(user.Role).filter(user.Role.name == "buyer").first()

    if not buyer_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default buyer role is not configured",
        )

    # Create local user
    new_user = user.User(
        authentik_sub=authentik_sub,
        email=email,
    )

    # Assign buyer role
    new_user.user_roles.append(user.UserRole(role=buyer_role))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
