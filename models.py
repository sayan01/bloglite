from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)
db.init_app(app)

# Creating Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(512))
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50))
    about = db.Column(db.String(256), nullable=False)
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'username: {self.username}\nName: {self.fname} {self.lname}'


with app.app_context():
    db.create_all()
