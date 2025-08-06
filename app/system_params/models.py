from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# System parameter model for managing application settings
class SystemParameter(db.Model):
    __tablename__ = 'system_parameters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)

    def __repr__(self):
        return f'<SystemParameter {self.name}>'