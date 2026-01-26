"""
User CRUD operations.

Handles user creation, authentication, and profile updates.
"""

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.users import User, UserCreate, UserUpdate


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Get a user by their email address."""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(*, session: Session, user_id: int) -> User | None:
    """Get a user by their ID."""
    return session.get(User, user_id)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password."""
    db_user = User(
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate_user(*, session: Session, email: str, password: str) -> User | None:
    """
    Authenticate a user by email and password.

    Returns the user if credentials are valid, None otherwise.
    """
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user(*, session: Session, db_user: User, user_update: UserUpdate) -> User:
    """
    Update a user's profile.

    Only updates fields that are actually provided (not None).
    Handles password hashing automatically.
    """
    update_data = user_update.model_dump(exclude_unset=True)

    # Handle password separately (needs hashing)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Update all provided fields
    for field, value in update_data.items():
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
