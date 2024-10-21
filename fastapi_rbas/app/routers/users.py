from fastapi import APIRouter, Depends
from app.services.user_service import assign_role, remove_role

router = APIRouter()

@router.post("/assign-role")
def assign_role_to_user(user_id: int, role_id: int):
    return assign_role(user_id, role_id)

@router.delete("/remove-role")
def remove_role_from_user(user_id: int, role_id: int):
    return remove_role(user_id, role_id)
