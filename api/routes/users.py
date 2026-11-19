from fastapi import APIRouter, Depends
from schema import user
from auth import dependencies

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
