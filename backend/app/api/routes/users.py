"""
User management routes.

Following FastAPI full-stack template pattern.
"""
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.models import User, UserPublic, UsersPublic, UserUpdate, Message

router = APIRouter()


@router.get("/", response_model=UsersPublic)
def read_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100
) -> UsersPublic:
    """
    Retrieve users (with pagination).
    """
    count_statement = select(User)
    users = session.exec(count_statement.offset(skip).limit(limit)).all()
    count = len(session.exec(count_statement).all())

    return UsersPublic(data=users, count=count)


@router.get("/{user_id}", response_model=UserPublic)
def read_user(session: SessionDep, user_id: int) -> User:
    """
    Get user by ID.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    session: SessionDep,
    current_user: CurrentUser,
    user_in: UserUpdate
) -> User:
    """
    Update current user.
    """
    if user_in.name is not None:
        current_user.name = user_in.name
    if user_in.email is not None:
        # Check if email is already taken
        existing = session.exec(
            select(User).where(User.email == user_in.email)
        ).first()
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_in.email

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/{user_id}", response_model=Message)
def delete_user(
    session: SessionDep,
    current_user: CurrentUser,
    user_id: int
) -> Message:
    """
    Delete user (self-deletion or admin).
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Only allow deleting self or if superuser
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
