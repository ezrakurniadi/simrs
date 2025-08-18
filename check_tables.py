from app import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables in database:")
    for table in tables:
        print(f"  - {table}")
        
    # Check columns in patient table
    if 'patient' in tables:
        columns = inspector.get_columns('patient')
        print("\nColumns in patient table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
            
    # Check columns in nationalities table
    if 'nationalities' in tables:
        columns = inspector.get_columns('nationalities')
        print("\nColumns in nationalities table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")