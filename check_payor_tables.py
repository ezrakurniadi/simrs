from app import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    
    # Check columns in payor_types table
    if 'payor_types' in inspector.get_table_names():
        columns = inspector.get_columns('payor_types')
        print("\nColumns in payor_types table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
    
    # Check columns in payor_details table
    if 'payor_details' in inspector.get_table_names():
        columns = inspector.get_columns('payor_details')
        print("\nColumns in payor_details table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
    
    # Check columns in id_types table
    if 'id_types' in inspector.get_table_names():
        columns = inspector.get_columns('id_types')
        print("\nColumns in id_types table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")