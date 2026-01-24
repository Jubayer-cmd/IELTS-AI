"""
CRUD operations.

Following FastAPI full-stack template pattern.
Reusable database operations for models.
"""
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, Essay, EssayCreate


# ═══════════════════════════════════════════════════════════════
# USER CRUD
# ═══════════════════════════════════════════════════════════════

def create_user(*, session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password."""
    db_user = User(
        name=user_create.name,
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Get user by email address."""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(*, session: Session, user_id: int) -> User | None:
    """Get user by ID."""
    return session.get(User, user_id)


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> User:
    """Update user fields."""
    user_data = user_in.model_dump(exclude_unset=True)

    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

    for field, value in user_data.items():
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """Authenticate user by email and password."""
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ═══════════════════════════════════════════════════════════════
# ESSAY CRUD
# ═══════════════════════════════════════════════════════════════

def create_essay(*, session: Session, essay_in: EssayCreate, user_id: int) -> Essay:
    """Create a new essay for a user."""
    word_count = len(essay_in.text.split())

    db_essay = Essay(
        text=essay_in.text,
        task_type=essay_in.task_type,
        word_limit=essay_in.word_limit,
        user_id=user_id,
        word_count=word_count,
    )
    session.add(db_essay)
    session.commit()
    session.refresh(db_essay)
    return db_essay


def get_essays_by_user(
    *, session: Session, user_id: int, skip: int = 0, limit: int = 20
) -> list[Essay]:
    """Get essays for a specific user with pagination."""
    statement = (
        select(Essay)
        .where(Essay.user_id == user_id)
        .order_by(Essay.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def get_essay_by_id(*, session: Session, essay_id: int) -> Essay | None:
    """Get essay by ID."""
    return session.get(Essay, essay_id)


def delete_essay(*, session: Session, essay: Essay) -> None:
    """Delete an essay."""
    session.delete(essay)
    session.commit()
