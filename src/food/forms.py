from datetime import datetime, date
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, IntegerField, EmailField, SelectField, BooleanField, SubmitField, DateTimeField, DateField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, URL, Email
from flask_wtf.file import FileField

NUM_PEOPLES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')]
categories = ['Pratos', 'Sucos', 'Bebidas', 'Café']

class BookForm(Form):
    name = StringField('Nome e Sobrenome', validators=[DataRequired()])
    phone = StringField('Telefone', validators=[DataRequired()])
    bdate  = DateField('Data', default=datetime.now())
    btime  = TimeField('Horário', default=datetime.now())
    num_peoples = SelectField('Nº de Pessoas', choices=NUM_PEOPLES)
    special = TextAreaField('Pedido Especial')
    submit = SubmitField('Enviar')

class MenuForm(Form):
    name = StringField('Nome', validators=[DataRequired()])
    category = SelectField('Categoria', choices=categories)
    desc = TextAreaField('Descrição', validators=[DataRequired()])
    pic = FileField('Imagem')
    price = StringField('Valor', validators=[DataRequired()])
    submit = SubmitField(u'Upload')
