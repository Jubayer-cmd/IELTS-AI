"""
Authentication API routes.

Handles user registration, login, and profile management.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.core.security import create_access_token
from app.models.users import Token, UserCreate, UserPublic, UserUpdate

router = APIRouter()


@router.post("/register", response_model=UserPublic)
def register_user(user_create: UserCreate, session: SessionDep):
    """
    Register a new user.

    - Checks if email is already registered
    - Hashes the password before storing
    - Returns the public user data
    """
    existing_user = crud.get_user_by_email(session=session, email=user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(session=session, user_create=user_create)
    return UserPublic.model_validate(user)


@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible login endpoint.

    Note: OAuth2 uses 'username' field, but we treat it as email.
    """
    user = crud.authenticate_user(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
def get_me(current_user: CurrentUser):
    """
    Get current logged-in user.

    This endpoint requires authentication.
    The CurrentUser dependency validates the JWT and returns the user.
    """
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_me(data: UserUpdate, session: SessionDep, current_user: CurrentUser):
    """
    Update current logged-in user's profile.

    Allows updating first name, last name, email, password.
    Only updates fields that are actually sent in the request.
    """
    updated_user = crud.update_user(
        session=session,
        db_user=current_user,
        user_update=data,
    )
    return updated_user
