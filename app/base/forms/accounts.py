from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Email, DataRequired


# Form that is presented to user on the login page
class LoginForm(FlaskForm):
    username = TextField('Username', id='username_login',
                         validators=[DataRequired()])

    password = PasswordField('Password', id='pwd_login',
                             validators=[DataRequired()])


# Form that is presented to user on the registration page
class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create',
                         validators=[DataRequired()])

    email = TextField('Email', id='email_create',
                      validators=[DataRequired(), Email()])

    first_name = TextField('First Name', id='first_name_create',
                           validators=[DataRequired()])

    last_name = TextField('Last Name', id='last_name_create',
                          validators=[DataRequired()])

    password = PasswordField('Password', id='pwd_create',
                             validators=[DataRequired()])
