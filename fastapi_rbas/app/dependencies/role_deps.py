from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.role_model import Role
from app.database import get_db
from app.dependencies.auth_deps import get_current_user

def role_required(required_role: str):
    """
    Dependency to check if the current user has the required role.

    Args:
        required_role (str): The role required to access the endpoint.

    Raises:
        HTTPException: If the user does not have the required role.
    """
    def role_checker(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Check if the user has the required role
        user_roles = db.query(Role).join(User.roles).filter(User.id == current_user.id).all()

        if not any(role.name == required_role for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required role to access this resource"
            )

        return current_user  # If user has the role, return the current user

    return role_checker
