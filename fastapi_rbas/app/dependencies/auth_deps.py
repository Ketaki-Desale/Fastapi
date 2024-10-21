from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.security import decode_access_token
from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schemas import UserOut  # Assuming you have a UserOut schema for output
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Define your token URL here

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOut:
    """
    Retrieve the current user from the JWT token.

    Args:
        token (str): The JWT token from the request.
        db (Session): The database session.

    Returns:
        UserOut: The current user object.

    Raises:
        HTTPException: If the token is invalid or user is not found.
    """
    # Decode the JWT token to get user information
    payload = decode_access_token(token)

    # Retrieve the user ID from the decoded payload
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    # Retrieve the user from the database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserOut.from_orm(user)  # Assuming you have a Pydantic schema for User
