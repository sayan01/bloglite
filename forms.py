from flask_wtf import *
from wtforms import *
from wtforms.validators import *

# Login Form Class
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
        Length(max=32)])
    password = PasswordField("Password", validators=[DataRequired(), 
        Length(min=8,
        message="Password should be atleast 8 characteres long")])
    submit = SubmitField("Login")


# Form Class Register
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
        Length(max=32)])
    password = PasswordField("Password", validators=[DataRequired(), 
        Length(min=8,
        message="Password should be atleast 8 characteres long")])
    fname = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    lname = StringField("Last Name", validators=[Length(max=50)])
    about = StringField("About (Bio)", validators=[DataRequired(), Length(max=256)])
    submit = SubmitField("Login")
