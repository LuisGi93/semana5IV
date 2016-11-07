# Import Form and RecaptchaField (optional)
from flask_wtf import Form
from wtforms.fields import TextField, BooleanField, PasswordField, TextAreaField
# Import Form elements such as TextField and BooleanField (optional)


# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])

class RegisterForm(Form):
    username = TextField('Name', [
                Required(message='Introduce an username')])
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])


class RecipeForm(Form):
    titulo = TextField('Titulo', [
                Required(message='Must provide a title. ;-)')])
    descripcion    = TextAreaField('Introduce the recipe description:', [
                Required(message='You must introduce a description')])
