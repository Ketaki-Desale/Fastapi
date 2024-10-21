from fastapi import Request, HTTPException, status
from fastapi.middleware import Middleware
from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.dependencies.auth_deps import get_current_user
from app.models.role_model import Role
from app.database import get_db

class RBACMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next):
        # Retrieve the required role from the request state or headers (this is just an example)
        required_role = request.headers.get("X-Required-Role")  # Custom header for role check

        if required_role:
            # Get current user using the dependency
            db: Session = get_db()
            current_user = await get_current_user(request.headers.get("Authorization").split(" ")[1], db)

            # Fetch the roles of the current user
            user_roles = db.query(Role).join(current_user.roles).filter(Role.name == required_role).all()

            if not user_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have the required role to access this resource"
                )

        response = await call_next(request)
        return response

# Usage in your FastAPI application
def create_app() -> FastAPI:
    app = FastAPI(middleware=[Middleware(RBACMiddleware)])

    # Include your routes here
    return app
