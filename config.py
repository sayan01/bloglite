from dotenv import load_dotenv
from app import app
from os import getenv

# config
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
