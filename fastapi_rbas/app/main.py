from fastapi import FastAPI
from app.routers import auth, users, roles, profile

app = FastAPI()

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])

@app.get("/")
def root():
    return {"message": "Welcome to the RBAC FastAPI App"}
