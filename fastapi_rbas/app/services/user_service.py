from app.models.user_role_model import UserRole
from app.models.user_model import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.database import get_db
from app.schemas.user_schemas import UserResponse

def assign_role(user_id: int, role_id: int, db: Session) -> None:
    """
    Assign a role to a user.

    Args:
        user_id (int): The ID of the user.
        role_id (int): The ID of the role to assign.
        db (Session): The database session.

    Raises:
        HTTPException: If the user or role does not exist.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()

def remove_role(user_id: int, role_id: int, db: Session) -> None:
    """
    Remove a role from a user.

    Args:
        user_id (int): The ID of the user.
        role_id (int): The ID of the role to remove.
        db (Session): The database session.

    Raises:
        HTTPException: If the user or role does not exist.
    """
    user_role = db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id).first()
    if not user_role:
        raise HTTPException(status_code=404, detail="UserRole association not found")

    db.delete(user_role)
    db.commit()

def get_current_user(db: Session = Depends(get_db), username: str = None) -> UserResponse:
    """
    Retrieve the current logged-in user based on the provided username.

    Args:
        db (Session): The database session.
        username (str): The username of the current user.

    Returns:
        UserResponse: The current user's data.

    Raises:
        HTTPException: If the user is not found.
    """
    if username is None:
        raise HTTPException(status_code=400, detail="Username must be provided")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.from_orm(user)
