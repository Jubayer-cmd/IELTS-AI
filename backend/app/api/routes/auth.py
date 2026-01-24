"""
Authentication routes.

Following FastAPI full-stack template pattern.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import User, UserCreate, UserPublic, Token, Message

router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(*, session: SessionDep, user_in: UserCreate) -> User:
    """
    Register a new user.
    """
    # Check if email already exists
    user = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Create user with hashed password
    user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login.

    Get an access token for future requests.
    """
    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    return Token(access_token=access_token)


@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: CurrentUser) -> User:
    """
    Get current user.
    """
    return current_user


@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> User:
    """
    Test access token.
    """
    return current_user
