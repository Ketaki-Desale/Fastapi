from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.services.auth_service import create_user, login_user
from app.database import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    User registration endpoint.

    Args:
        user (UserCreate): User registration data.
        db (Session): Database session.

    Returns:
        User: The created user object.
    """
    return create_user(user, db)  # Pass the db parameter here

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    """
    User login endpoint.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        db (Session): Database session.

    Returns:
        str: JWT access token.
    """
    return login_user(username, password, db)
