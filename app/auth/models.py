import uuid
from flask_login import UserMixin
import bcrypt
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Text
from app import db  # Import the SQLAlchemy instance from app/__init__.py

# Association table for many-to-many relationship between User and Role
user_roles = db.Table('user_roles',
    db.Column('user_id', db.String(36), db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.String(36), db.ForeignKey('role.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases

    # Many-to-many relationship with roles
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def set_password(self, password):
        # Hash a password with bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        # Check a hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def has_role(self, *roles):
        """
        Check if the user has any of the specified roles.

        Args:
            *roles: Variable number of role names as strings

        Returns:
            bool: True if user has any of the specified roles, False otherwise
        """
        if not self.roles:
            return False

        user_roles = [role.name for role in self.roles]
        return any(role in user_roles for role in roles)

class Role(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.String(36))  # User ID of creator
    updated_by = db.Column(db.String(36))  # User ID of last updater
    additional_data = db.Column(JSONB)  # JSONB column for additional data (PostgreSQL) or JSON for other databases


