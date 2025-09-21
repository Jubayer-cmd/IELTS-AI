# Database initialization script
# TODO: Create all database tables and initial data

from sqlalchemy import create_engine
from ..core.database import Base
from ..core.config import settings
from ..models import user, essay, evaluation, payment

def init_database():
    """Initialize database with all tables"""
    engine = create_engine(settings.database_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def create_admin_user():
    """Create initial admin user"""
    # TODO: Implement admin user creation
    pass

if __name__ == "__main__":
    init_database()
    create_admin_user()
