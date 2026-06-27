import sys
import os

# Add the backend directory to the path so we can import modules reliably
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.database import DATABASE_URL, init_db, SessionLocal
from app.core.security import get_password_hash
from app.models.models import User, UserRole

def create_initial_data():
    admin_password = os.getenv("INITIAL_ADMIN_PASSWORD")
    if not admin_password:
        raise RuntimeError("INITIAL_ADMIN_PASSWORD environment variable is required")

    db = SessionLocal()
    try:
        # Check if super admin exists
        admin = db.query(User).filter(User.email == "admin@buxgalter.uz").first()
        if not admin:
            print("Creating super admin user...")
            admin = User(
                email="admin@buxgalter.uz",
                hashed_password=get_password_hash(admin_password),
                full_name="System Administrator",
                role=UserRole.SUPER_ADMIN
            )
            db.add(admin)
            db.commit()
            print("Super admin created successfully.")
        else:
            print("Super admin already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database tables...")
    print(f"Using database: {DATABASE_URL}")
    try:
        init_db()
        print("Tables created successfully.")
        create_initial_data()
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error initializing database: {e}")
