from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired

class new_user_form(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])

class user_login(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class user_feedback(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])
    