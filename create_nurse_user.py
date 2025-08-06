"""
Nurse User Creation Script
Extends create_user.py functionality to handle nurse-specific validation
"""

from app.auth.models import User, Role, db
from flask import Flask
import bcrypt

def create_nurse_user(username: str, email: str, first_name: str, last_name: str, password: str) -> dict:
    """
    Create a new nurse user with unique validation
    
    Args:
        username: Nurse's username
        email: Nurse's email
        first_name: Nurse's first name
        last_name: Nurse's last name
        password: Password to set
        
    Returns:
        dict: Operation result with success status and message
    """
    # Check for existing nurse entries
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {"success": False, "message": f"Username '{username}' already exists"}
    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return {"success": False, "message": f"Email '{email}' already exists"}
    
    # Create nurse role if not exists
    nurse_role = Role.query.filter_by(name='Nurse').first()
    if not nurse_role:
        nurse_role = Role(name='Nurse', description='Nurse role')
        db.session.add(nurse_role)
    
    # Create user with nurse role
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    
    # Set password and assign role
    user.set_password(password)
    user.roles.append(nurse_role)
    
    try:
        db.session.add(user)
        db.session.commit()
        return {"success": True, "message": "Nurse user created successfully", "user": user.username}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Creation failed: {str(e)}"}

# Test block for sample scenarios
if __name__ == "__main__":
    # Create Flask app context with proper PostgreSQL credentials
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/simrs_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Test 1: Successful nurse creation
        result = create_nurse_user(
            username='nurse1',
            email='nurse1@example.com',
            first_name='Nurse',
            last_name='One',
            password='securepassword'
        )
        print("\nTEST 1 - Successful Creation:")
        print(result)
        
        # Test 2: Duplicate username
        result = create_nurse_user(
            username='nurse1',
            email='nurse1_duplicate@example.com',
            first_name='Nurse',
            last_name='One',
            password='securepassword'
        )
        print("\nTEST 2 - Duplicate Username:")
        print(result)
        
        # Test 3: Duplicate email
        result = create_nurse_user(
            username='nurse2',
            email='nurse1@example.com',
            first_name='Nurse',
            last_name='Two',
            password='securepassword'
        )
        print("\nTEST 3 - Duplicate Email:")
        print(result)
        
        # Test 4: Original create_user functionality (backward compatibility)
        from app.admin.models import User as AdminUser
        admin_result = AdminUser.create_user(
            username='admin1',
            email='admin1@example.com',
            first_name='Admin',
            last_name='One',
            password='adminpass',
            role='Admin'
        )
        print("\nTEST 4 - Original Admin User Creation:")
        print(admin_result)