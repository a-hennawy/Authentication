from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.init_app(app)
    app.app_context().push()
    return db


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         unique=True)
    password = db.Column(db.Text,
                         nullable=False)

    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    @classmethod
    def register(cls, username, password, email,
                 first_name, last_name):
        hashed_password = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_password.decode("utf8")
        registered_user = cls(username=username, password=hashed_utf8,
                   email=email, first_name=first_name,
                   last_name=last_name)
        db.session.add(registered_user)
        db.session.commit()
        return registered_user

    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
        else:
            return False
        
        if is_auth:
            return user
        else:
            return False
    
    feedback = db.relationship("Feedback", backref="users", cascade="all,delete")

class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, auto_incrementing=False)

    title = db.Column(db.String(100), nullable=False, )

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text,  db.ForeignKey('users.username'))

    @classmethod
    def add_feedback(cls, title, content, username):
        feedback= cls(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return feedback


