from fastapi import APIRouter
from app.services.role_service import create_role, get_roles
from app.schemas.role_schemas import RoleCreate

router = APIRouter()

@router.post("/")
def create_new_role(role: RoleCreate):
    return create_role(role)

@router.get("/")
def list_roles():
    return get_roles()
