from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

# Creating Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(512), nullable=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=True)
    about = db.Column(db.String(256), nullable=False)
    joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readible attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(pwhash=self.passhash, password=password)
    
    def __repr__(self) -> str:
        return super().__repr__()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(512), nullable=True)
    author = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


with app.app_context():
    db.create_all()
