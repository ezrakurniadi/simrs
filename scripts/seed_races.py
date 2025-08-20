from app import create_app
from app.system_params.models import Race
from app import db

def seed_races():
    app = create_app()
    with app.app_context():
        # List of races to add
        races = [
            'American Indian or Alaska Native',
            'Asian',
            'Black or African American',
            'Hispanic or Latino',
            'Native Hawaiian or Other Pacific Islander',
            'White',
            'Other',
            'Prefer not to say'
        ]
        
        for race_name in races:
            # Check if race already exists
            existing_race = Race.query.filter_by(name=race_name).first()
            if not existing_race:
                race = Race(
                    name=race_name,
                    created_at=db.func.current_timestamp(),
                    updated_at=db.func.current_timestamp()
                )
                db.session.add(race)
                print(f"Added race: {race_name}")
        
        db.session.commit()
        print("Race seeding completed!")

if __name__ == '__main__':
    seed_races()