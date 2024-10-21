from passlib.context import CryptContext
from jose import JWTError, jwt
from app.config import JWT_SECRET, JWT_ALGORITHM
from datetime import datetime, timedelta

# Create a CryptContext object for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """
    Hash a password.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The payload data for the token.
        expires_delta (timedelta, optional): The expiration time for the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiration time
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
