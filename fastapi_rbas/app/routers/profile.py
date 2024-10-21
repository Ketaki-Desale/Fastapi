from fastapi import APIRouter, Depends
from app.schemas.user_schemas import UserResponse
from app.services.user_service import get_current_user

router = APIRouter()

@router.get("/", response_model=UserResponse)
def get_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user
