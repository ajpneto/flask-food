from flask_wtf import FlaskForm as Form
from wtforms import StringField, IntegerField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL, Email
from .models import User
from . import authenticate


class RegisterForm(Form):
    name = StringField('Nome e Sobrenome', validators=[DataRequired(), Length(max=255)])
    age = IntegerField('Idade', validators=[DataRequired()])
    address = StringField('Endereço', validators=[DataRequired(), Length(max=255)])
    phone = StringField('Celular com DDD', validators=[DataRequired(), Length(max=11)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    cpassword = PasswordField('Confirme sua Senha', validators=[
        DataRequired(),
        EqualTo('password')
    ])


    def validate(self, extra_validators=None):
        check_validate = super(RegisterForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        phone = User.query.filter_by(phone=self.phone.data).first()

        # Is the username already being used
        if phone:
            self.phone.errors.append("Usuário cadastrado, faça login ou tente cadastrar outro número")
            return False

        return True


class LoginForm(Form):
    phone = StringField('Celular', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField("Lembrar")

    def validate(self,  extra_validators=None):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our user exist
        user = User.query.filter_by(phone=self.phone.data).first()
        if not user:
            self.phone.errors.append('Número de telefone ou Senha inválidos')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.password.errors.append('Número de telefone ou Senha inválidos')
            return False

        return True
