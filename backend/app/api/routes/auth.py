from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # 👈 Add this
from sqlmodel import select, Session

from app.api.deps import SessionDep, CurrentUser
from app.models.users import User, UserCreate, UserPublic, Token, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserPublic)
def register_user(
    user_create: UserCreate,
    session: SessionDep
):
    """
    Register a new user.

    - Hashes the password before storing.
    - Returns the public user data.
    """
    existing_user = session.exec(
        select(User).where(User.email == user_create.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_create.password)
    new_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        first_name=user_create.first_name,
        last_name=user_create.last_name
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return UserPublic.model_validate(new_user)

@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()  # 👈 Form data, not query params
):
    """
    OAuth2 compatible login endpoint.

    Note: OAuth2 uses 'username' field, but we treat it as email.
    """
    # OAuth2 uses 'username', but we use email
    email = form_data.username
    password = form_data.password

    # Find user by email
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
def get_me(current_user: CurrentUser):
    """
    Get current logged-in user.

    This endpoint requires authentication.
    The CurrentUser dependency:
    1. Extracts JWT token from "Authorization: Bearer <token>" header
    2. Decodes the token to get user ID
    3. Fetches the user from database
    4. Returns the user object (or 401 if invalid)
    """
    return current_user

@router.patch("/me", response_model=UserPublic)
def update_me(data: UserUpdate, session: SessionDep, current_user: CurrentUser):
    """
    Update current logged-in user's profile.

    Allows updating first name, last name, email, password.
    Only updates fields that are actually sent in the request.
    """
    # Get only fields user actually sent (exclude None values)
    update_data = data.model_dump(exclude_unset=True)

    # Handle password separately (needs hashing)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Update all fields at once
    for field, value in update_data.items():
        setattr(current_user, field, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
