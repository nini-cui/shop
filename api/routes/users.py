from fastapi import APIRouter, Depends, HTTPException
from schema import user
from api.auth import dependencies
from sqlalchemy.orm import Session
from db import deps

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(
    current_user: user.User = Depends(dependencies.get_current_user),
):
    return {
        "id": current_user.id,
        "authentik_sub": current_user.authentik_sub,
        "roles": [user_role.role.name for user_role in current_user.user_roles],
    }


@router.post("/create_user")
def create_user(
    payload: dict = Depends(dependencies.verify_token),
    db: Session = Depends(deps.get_db),
):
    auth_sub = payload.get("sub")
    email = payload.get("email")

    if not auth_sub or not email:
        raise HTTPException(
            status_code=400,
            detail="Token is missing sub or email",
        )

    current_user = (
        db.query(user.User).filter(user.User.authentik_sub == auth_sub).first()
    )

    if current_user:
        return {"message": "User already exists"}

    new_user = user.User(
        authentik_sub=auth_sub,
        email=email,
    )

    default_role = db.query(user.Role).filter(user.Role.name == "buyer").first()

    if not default_role:
        raise HTTPException(
            status_code=500,
            detail="Default role not found",
        )

    new_user.user_roles.append(user.UserRole(role=default_role))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}
