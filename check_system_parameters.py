from app import create_app, db
from app.system_params.models import Ethnicity, Language

app = create_app()

with app.app_context():
    # Check ethnicities
    ethnicities = Ethnicity.query.all()
    print(f"Ethnicities count: {len(ethnicities)}")
    for ethnicity in ethnicities:
        print(f"  - {ethnicity.name}")
    
    # Check languages
    languages = Language.query.all()
    print(f"Languages count: {len(languages)}")
    for language in languages:
        print(f"  - {language.name} ({language.iso_code})")