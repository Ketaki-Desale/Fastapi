from app.models.role_model import Role
from sqlalchemy.orm import Session
from fastapi import HTTPException

def create_role(role_data: dict, db: Session) -> Role:
    """
    Create a new role in the database.

    Args:
        role_data (dict): A dictionary containing role details.
        db (Session): The database session.

    Returns:
        Role: The created role object.

    Raises:
        HTTPException: If the role already exists.
    """
    # Check if the role already exists
    existing_role = db.query(Role).filter(Role.name == role_data['name']).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    # Create a new role
    new_role = Role(name=role_data['name'], description=role_data.get('description'))
    db.add(new_role)
    db.commit()
    db.refresh(new_role)  # Refresh to get the updated role object with the ID

    return new_role

def get_roles(db: Session) -> list:
    """
    List all roles in the database.

    Args:
        db (Session): The database session.

    Returns:
        list: A list of all roles.
    """
    roles = db.query(Role).all()
    return roles
