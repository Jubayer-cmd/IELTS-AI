# JWT authentication and password hashing
# TODO: Implement JWT token creation, verification, and password handling

from datetime import datetime, timedelta
import hashlib
import os

# Try to import jose and passlib, but make them optional for MVP
try:
    from jose import JWTError, jwt
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    JWT_AVAILABLE = True
except ImportError:
    # Fallback for MVP - simple hashing
    JWT_AVAILABLE = False
    print("Warning: JWT dependencies not installed. Using simple hashing for MVP.")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    if JWT_AVAILABLE:
        return pwd_context.verify(plain_password, hashed_password)
    else:
        # Simple fallback for MVP
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password"""
    if JWT_AVAILABLE:
        return pwd_context.hash(password)
    else:
        # Simple fallback for MVP
        return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    if JWT_AVAILABLE:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, "secret-key", algorithm="HS256")
    else:
        # Simple fallback for MVP
        return f"mock_token_{data.get('sub', 'user')}"

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    if JWT_AVAILABLE:
        try:
            payload = jwt.decode(token, "secret-key", algorithms=["HS256"])
            return payload
        except JWTError:
            return None
    else:
        # Simple fallback for MVP
        if token.startswith("mock_token_"):
            return {"sub": token.replace("mock_token_", "")}
        return None
