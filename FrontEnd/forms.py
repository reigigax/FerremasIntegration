from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    buy_order = StringField('Orden de Compra', validators=[DataRequired()])
    session = StringField('Sesion', validators=[DataRequired()])
    amount = IntegerField('Monto', validators=[DataRequired()])

    submit = SubmitField('Realizar Compra')
