from app import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    
    # Check columns in user_roles table
    if 'user_roles' in inspector.get_table_names():
        columns = inspector.get_columns('user_roles')
        print("\nColumns in user_roles table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")