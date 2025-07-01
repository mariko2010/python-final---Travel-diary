from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileField, FileSize

class BlogForm(FlaskForm):
    image = FileField("ატვირთე ფოტო",  validators=[FileSize(1024 * 1024 * 4)])
    name = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    add_blog = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), length(min=8, max=64)])
    register_button = SubmitField()

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    login_button = SubmitField()
