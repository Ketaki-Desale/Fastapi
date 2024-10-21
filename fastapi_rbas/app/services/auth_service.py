from app.models.user_model import User
from app.utils.security import verify_password, hash_password, create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.user_schemas import UserCreate, UserResponse

def create_user(user_data: UserCreate, db: Session) -> UserResponse:
    """
    Create a new user in the database.
    
    Args:
        user_data (UserCreate): The user data provided during registration.
        db (Session): The database session.

    Returns:
        UserResponse: The created user's data.
    """
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Create a new User instance
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),  # Hash the password
    )

    # Add the new user to the session and commit to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)

def login_user(username: str, password: str, db: Session) -> str:
    """
    Authenticate a user and create a JWT token.
    
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        db (Session): The database session.

    Returns:
        str: The JWT token for the authenticated user.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Create a JWT token for the user
    access_token = create_access_token(data={"sub": user.username})

    return access_token
