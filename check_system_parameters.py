from app import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    
    # Check columns in system_parameters table
    if 'system_parameters' in inspector.get_table_names():
        columns = inspector.get_columns('system_parameters')
        print("\nColumns in system_parameters table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")