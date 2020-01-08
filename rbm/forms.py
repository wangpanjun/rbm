# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    key = StringField('key', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
