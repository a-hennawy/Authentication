from flask import Flask, redirect, render_template, flash, session, request
from models import db, connect_db, User, Feedback
from forms import new_user_form, user_login, user_feedback
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mac@localhost:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

db = connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/login')

@app.route('/register', methods=["GET", "POST"])
def register():

    form = new_user_form()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
  
        User.register(username, password, email, first_name, last_name)    
        
        flash(f"Welcome, {username} you have successfully created your account")
        return redirect(f'/users/{username}')
    else:

        return render_template('register.html.j2', form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    form = user_login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            flash(f"Successfully logged in as {username}")    
            return redirect(f'/users/{user.username}')
            
        else:
            form.username.errors={'username':["username or password incorrect"]}
            return render_template('login.html.j2', form=form)
    else:
        return render_template('login.html.j2', form=form)
@app.route('/users/<username>')
def user_page(username):
    
    if username not in session['username']:
        flash("you must be logged in to view")
        return redirect("/")
    else:
        flash(f"hi, {session['username']}")
        logged_user = User.query.filter_by(username=username).first()
        feedbacks =logged_user.feedback
        return render_template("user-page.html.j2", logged_user=logged_user,
                               feedbacks=feedbacks)

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect("/")


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if username not in session['username'] or username != session['username']:
        raise Unauthorized
    user_to_delete = db.session.query(User, Feedback).join(Feedback).filter_by(username = username).all()
    db.session.delete(user_to_delete[0][0])
    db.session.commit()
    session.pop("username")

    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['POST', 'GET'])
def add_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    form = user_feedback()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        Feedback.add_feedback(title, content, username)
        return redirect(f"/users/{username}")
    else:
        return render_template("feedback-form.html.j2", form=form)

    
