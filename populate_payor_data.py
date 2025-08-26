import os
import sys
from app import create_app, db
from app.system_params.models import PayorType, PayorDetail
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def populate_payor_data():
    app = create_app()
    with app.app_context():
        # Check if payor types already exist
        existing_payor_types = PayorType.query.all()
        if existing_payor_types:
            print(f"Found {len(existing_payor_types)} existing payor types. Skipping population.")
            return
        
        # Define payor types
        payor_types_data = [
            {"name": "Insurance", "description": "Insurance companies"},
            {"name": "Company", "description": "Corporate accounts"},
            {"name": "Stakeholder", "description": "Government or NGO accounts"}
        ]
        
        # Add payor types
        payor_types = []
        for pt_data in payor_types_data:
            payor_type = PayorType(
                name=pt_data["name"],
                description=pt_data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(payor_type)
            payor_types.append(payor_type)
        
        # Commit to get IDs
        db.session.commit()
        
        # Define payor details for each type
        payor_details_data = [
            # Insurance details
            {"name": "BPJS", "description": "Badan Penyelenggara Jaminan Sosial", "payor_type_id": payor_types[0].id},
            {"name": "AdMedika", "description": "AdMedika Insurance", "payor_type_id": payor_types[0].id},
            {"name": "Aetna", "description": "Aetna Insurance", "payor_type_id": payor_types[0].id},
            {"name": "Allianz", "description": "Allianz Insurance", "payor_type_id": payor_types[0].id},
            {"name": "Cigna", "description": "Cigna Insurance", "payor_type_id": payor_types[0].id},
            {"name": "Prudential", "description": "Prudential Insurance", "payor_type_id": payor_types[0].id},
            
            # Company details
            {"name": "PT. Medistra Hospital", "description": "Medistra Hospital Corporate Account", "payor_type_id": payor_types[1].id},
            {"name": "PT. Healthcare Corp", "description": "Healthcare Corporation", "payor_type_id": payor_types[1].id},
            {"name": "PT. Medical Solutions", "description": "Medical Solutions Provider", "payor_type_id": payor_types[1].id},
            {"name": "PT. Wellness Group", "description": "Wellness Group Corporate Account", "payor_type_id": payor_types[1].id},
            
            # Stakeholder details
            {"name": "Government", "description": "Government healthcare programs", "payor_type_id": payor_types[2].id},
            {"name": "NGO", "description": "Non-Governmental Organizations", "payor_type_id": payor_types[2].id},
            {"name": "Private Donor", "description": "Private healthcare donors", "payor_type_id": payor_types[2].id},
            {"name": "International Aid", "description": "International healthcare aid organizations", "payor_type_id": payor_types[2].id}
        ]
        
        # Add payor details
        for pd_data in payor_details_data:
            # Check if detail already exists
            existing = PayorDetail.query.filter_by(name=pd_data["name"]).first()
            if not existing:
                payor_detail = PayorDetail(
                    name=pd_data["name"],
                    description=pd_data["description"],
                    payor_type_id=pd_data["payor_type_id"],
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(payor_detail)
        
        # Commit all changes
        db.session.commit()
        print(f"Added {len(payor_types_data)} payor types and {len(payor_details_data)} payor details to the database.")

if __name__ == "__main__":
    populate_payor_data()