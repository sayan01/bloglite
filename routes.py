from flask import *
from flask_login import *
from models import *
from forms import *
from error import *
from datetime import timedelta
from app import app

@app.route('/')
@login_required
def home():
    posts = Post.query.order_by(Post.time)
    return render_template("index.html", posts=posts, homeactive="active", current_user=current_user)
    
# Users -------------------------------------------------------------------------------

@app.route('/user/search')
@login_required
def search():
    return render_template("search/index.html")

@app.route('/user/', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return render_template("user/index.html", 
    profileactive="active",
    users = users
    )

@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@fresh_login_required
def edit_user(id):
    form = UserForm()
    user = User.query.get_or_404(id)
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
@fresh_login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST' and request.form['sure']:
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f"User @{user.username} Deleted successfully")
            return redirect(location=url_for("get_users"))
        except Exception as e:
            flash("Error Occurred while deleting user")
            abort(500, description=e)
    elif request.form and not request.form['sure']: 
        flash("Please confirm that you are sure") 
    return render_template("user/delete.html", user = user)
        

@app.route('/user/login', methods=['GET','POST'])
def login():
    form = UserForm()
    # Validate Form
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash("User does not exist")
        elif user.verify_password(form.password.data):
            assert login_user(user, remember="remember" in request.form, duration=timedelta(days=30))
            return redirect(location=url_for("home"))
        else:
            flash('Login failed')
    return render_template("user/login.html", form = form, loginactive="active")

@app.route('/user/logout')
@login_required
def logout():
    try:
        assert logout_user()
        flash('You have been logged out')
        return redirect(location=url_for('login'))
    except Exception as e:
        abort(500, description=e)

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
@login_required
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


@app.route('/post/view/<int:id>')
@login_required
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template("post/view.html", post=post, homeactive="active")
    
@app.route('/post/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if request.method == 'GET' or not form.validate_on_submit():
        flash_form_errors(form)
        form.title.data = post.title
        form.caption.data = post.caption
        form.image.data = post.image
        return render_template("post/edit.html", form=form, post=post)
    else:
        try:
            post.title = form.title.data
            post.caption = form.caption.data
            post.image = form.image.data
            db.session.commit()
            flash("Post updated successfully")
            return redirect(location=url_for('view_post', id=post.id))
        except Exception as e:
            flash("Oops something went wrong!")
            abort(500, description=e)

@app.route('/post/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST' and request.form['sure']:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully")
            return redirect(location=url_for('home'))
        except Exception as e:
            abort(500, description=e)
    if request.form and not request.form['sure']: 
        flash("Please confirm that you are sure")
    return render_template('/post/delete.html', post=post)
        

# Error pages ------------------------------------------------------------------------------------
# invalid url
@app.errorhandler(404)
def error404(e):
    return render_template("error/404.html", error=e), 404
    
# internal error
@app.errorhandler(500)
def error500(e):
    return render_template("error/500.html", error=e), 500