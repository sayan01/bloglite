from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *

# Form Class Register
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
        Length(max=32)])
    password = PasswordField("Password", validators=[DataRequired(), 
        Length(min=8,
        message="Password should be atleast 8 characteres long")])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), 
        Length(min=8,
        message="Password should be atleast 8 characteres long"),
        EqualTo('password', message="Passwords must match")])
    fname = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    lname = StringField("Last Name", validators=[Length(max=50)])
    about = StringField("About (Bio)", validators=[DataRequired(), Length(max=256)])
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField("Title", 
        validators=[
            DataRequired(message="Title cannot be empty"), 
            Length(max=50, message="Title cannot be longer than 50 characters")
        ]
    )
    caption = StringField("Caption", 
        validators=[
            DataRequired(message="Caption cannot be empty"), 
            Length(max=200, message="Caption cannot be longer than 200 characters")
        ], 
        widget=TextArea()
    )
    image = FileField("Photo", validators=[])
    submit = SubmitField("Post")