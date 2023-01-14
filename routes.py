from flask import render_template, flash
from models import *
from forms import *
from auth import *
from app import app

@app.route('/')
def home():
    return render_template("index.html")
    
@app.route('/search')
def search():
    return render_template("search/index.html")

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    return render_template("user/index.html", 
    profileactive="active",
    user = {"username": "sayan", "fname": "Sayan", "lname": "Ghosh", "about": "I code stuff", "id": id})

@app.route('/login', methods=['GET','POST'])
def login():
    username, password = None, None
    form = LoginForm()
    # Validate Form
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.username.data = ''
        form.password.data = ''
        if password == "12345678":
            flash('Login successful')
        else:
            flash('Login failed')
    return render_template("user/login.html",
        username = username,
        password = password,
        form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    username, password, fname, lname, about = [None]*5
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('username already taken')
        else:
            username, password, fname, lname, about = form.username.data, form.password.data, form.fname.data, form.lname.data, form.about.data
            user = User(username=username, passhash=hashpass(username,password), fname=fname, lname=lname, about=about)
            db.session.add(user)
            db.session.commit()
            form.username.data, form.password.data, form.fname.data, form.lname.data, form.about.data = ['']*5
            flash('Registration Successful')
    users = User.query.order_by(User.joined)
    return render_template("user/register.html",
    username = username, password = password, fname = fname, lname = lname, about = about, form=form, users=users)

# error pages
# invalid url
@app.errorhandler(404)
def error404(e):
    return render_template("error/404.html", error=e), 404