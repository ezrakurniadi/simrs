from functools import wraps
from flask import abort, redirect
from flask_login import current_user


def roles_required(*roles):
    """
    Decorator for routes that require specific roles.
    
    Usage:
    @roles_required('Admin', 'Doctor')
    def some_route():
        # Only users with Admin OR Doctor role can access this
        pass
    
    Args:
        *roles: Variable number of role names as strings
        
    Returns:
        Decorated function that checks user roles before allowing access
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
                        if not current_user.is_authenticated:
                            abort(401)  # Unauthorized
                        
                        # Check if user has any of the required roles
                        if not current_user.has_role(*roles):
                            abort(403)
                            
                        return func(*args, **kwargs)
        return decorated_function
    return decorator