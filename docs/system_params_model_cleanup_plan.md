# System Parameters Model Cleanup Plan

## Issue
The `app/system_params/models.py` file contains duplicate `User` and `Role` classes that conflict with the ones defined in `app/auth/models.py`. This causes a SQLAlchemy error when the application tries to initialize.

## Solution
Remove the duplicate `User` and `Role` classes from `app/system_params/models.py`, keeping only the system parameter models that belong in this module.

## Files to Modify
`app/system_params/models.py` - Remove lines 9-57 which contain the duplicate User and Role classes

## Code to Remove
```python
class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))
    
    # Relationship with users - will be populated by auth/models.py

    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))
    
    # User preferences
    preferred_language = db.Column(db.String(10), default='en')
    
    # Relationships - will be populated by auth/models.py
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'
```

## Code to Keep
All other classes in the file should remain unchanged:
- SystemParameter
- PayorType
- PayorDetail
- IDType
- Ethnicity
- Language
- Helper functions

## Implementation Notes
1. Remove the duplicate classes but keep all imports
2. Keep the comment on line 7: "# Remove the user_roles table definition since it's defined in auth/models.py"
3. Ensure all other system parameter models remain intact