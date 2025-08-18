# User and Role Model Conflict Resolution

## Issue Description
The application is experiencing a SQLAlchemy error due to multiple classes named "Role" being defined in the declarative base registry:
1. `app/auth/models.py` - Role class (lines 56-64)
2. `app/system_params/models.py` - Role class (line 9)

This conflict prevents the application from initializing properly, causing the error:
```
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[User(user)]'. Original exception was: Multiple classes found for path "Role" in the registry of this declarative base. Please use a fully module-qualified path.
```

## Root Cause Analysis
The conflict occurs because both model files are being imported and both define a `Role` class that inherits from `db.Model`. When SQLAlchemy tries to resolve the relationship in the `User` model:
```python
roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                        backref=db.backref('users', lazy=True))
```

It cannot determine which `Role` class to use since there are two with the same name.

## Database Schema Analysis
Based on the existing code structure and imports, the correct models should be:
1. `User` and `Role` from `app/auth/models.py` (with proper relationships)
2. Other system parameter models from `app/system_params/models.py` (without duplicating User/Role)

## Solution Plan
1. Remove the duplicate `User` and `Role` classes from `app/system_params/models.py`
2. Ensure proper imports in `app/models/__init__.py`
3. Verify relationships are correctly defined
4. Test the application to ensure the conflict is resolved

## Implementation Steps
1. Edit `app/system_params/models.py` to remove the duplicate User and Role classes
2. Verify that `app/auth/models.py` contains the complete and correct User and Role models
3. Check that `app/models/__init__.py` properly imports the models
4. Test the application to confirm the issue is resolved

## Files to Modify
1. `app/system_params/models.py` - Remove duplicate User and Role classes
2. `app/models/__init__.py` - Verify imports (may not need changes)
3. `app/auth/models.py` - Verify completeness (may not need changes)