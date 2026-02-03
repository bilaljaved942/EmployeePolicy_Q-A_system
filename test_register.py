#!/usr/bin/env python
"""Test registration endpoint"""
import sys
sys.path.insert(0, '.')

from src.models import SessionLocal, User, Base, engine, init_db
from src.auth import create_user

# Initialize database
Base.metadata.create_all(bind=engine)

# Test registration
db = SessionLocal()

try:
    print("Testing user creation...")
    new_user = create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123",
        full_name="Test User"
    )
    print(f"✅ User created: {new_user}")
    print(f"   ID: {new_user.id}")
    print(f"   Username: {new_user.username}")
    print(f"   Email: {new_user.email}")
    print(f"   Created at: {new_user.created_at}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
