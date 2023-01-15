from flask import *
from models import *
from forms import *
from error import *
from app import app

@app.route('/')
def home():
    posts = Post.query.order_by(Post.time)
    return render_template("index.html", posts=posts)
    
# Users -------------------------------------------------------------------------------

@app.route('/user/search')
def search():
    return render_template("search/index.html")

@app.route('/user/', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template("user/index.html", 
    profileactive="active",
    users = users
    )

@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    form = UserForm()
    user = User.query.get_or_404(id)
    if not user:
        abort(404)
    if request.method == 'POST':
        print('validated on submit')
        user.fname, user.lname, user.about = form.fname.data, form.lname.data, form.about.data
        try:
            db.session.commit()
            flash('User Details Edit Successful')
            return redirect(location=url_for("get_users"))
        except Exception as e:
            flash('Some unknown error occured')
            abort(500)
    else:
        print("not validated")
        form.username.data, form.fname.data, form.lname.data, form.about.data = user.username, user.fname, user.lname, user.about
        return render_template("user/edit.html", profileactive="active", user = user, form = form)


@app.route('/user/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    if not user:
        abort(404)
    if request.method == 'GET' or not request.form['sure']:
        return render_template("user/delete.html", user = user)
    else:
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f"User @{user.username} Deleted successfully")
            return redirect(location=url_for("get_users"))
        except Exception as e:
            flash("Error Occurred while deleting user")
            print(e)
            abort(500)


@app.route('/user/login', methods=['GET','POST'])
def login():
    form = UserForm()
    # Validate Form
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            abort(404)
        if user.verify_password(form.password.data):
            flash('Login successful')
            return redirect(location=url_for("get_users"))
        else:
            flash('Login failed')
    return render_template("user/login.html",
        form = form,
        loginactive="active")

@app.route('/user/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                flash('username already taken')
            else:
                user = User(username=form.username.data, 
                    password=form.password.data, 
                    fname=form.fname.data, 
                    lname=form.lname.data, 
                    about=form.about.data
                )
                db.session.add(user)
                db.session.commit()
                flash('Registration Successful')
                return redirect(location=url_for("login"))
        else:
            flash_form_errors(form)
    return render_template("user/register.html", registeractive="active", form=form)


# Post ----------------------------------------------------------------------------------------

@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if request.method == 'GET' or not form.validate_on_submit():
        flash_form_errors(form)
        return render_template("post/add.html",form=form, createactive="active")
    else:
        post = Post(title=form.title.data, 
            caption=form.caption.data, 
            image=form.image.data, 
            author=User.query.first().username
        )
        try:
            db.session.add(post)
            db.session.commit()
            flash('Added post successfully')
            return redirect(location=url_for('home'))
        except Exception as e:
            flash("Something went wrong while adding post")
            abort(500, description=e)



# error pages
# invalid url
@app.errorhandler(404)
def error404(e):
    return render_template("error/404.html", error=e), 404
    
# internal error
@app.errorhandler(500)
def error500(e):
    return render_template("error/500.html", error=e), 500