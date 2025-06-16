from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class TransactionForm(FlaskForm):
    buy_order = StringField('Orden de Compra', validators=[DataRequired()])
    session = StringField('Sesion', validators=[DataRequired()])
    amount = IntegerField('Monto', validators=[DataRequired()])

    submit = SubmitField('Realizar Compra')

class AddProductToCartForm(FlaskForm):
    carrito_id_producto = IntegerField('Id Producto',validators=[DataRequired()])
    carrito_cantidad_producto = IntegerField('Cantidad',validators=[DataRequired(), Length(min=1)])

    submit = SubmitField('Añadir Producto')

class DeleteProductFromCartForm(FlaskForm):
    carrito_id_producto = IntegerField('Id Producto',validators=[DataRequired()])

    submit = SubmitField('Eliminar Producto')

class ModifyProductOnCartForm(FlaskForm):
    carrito_id_producto = IntegerField('Id Producto',validators=[DataRequired()])
    carrito_cantidad_producto = IntegerField('Cantidad',validators=[DataRequired()])

    submit = SubmitField('Actualizar')

class DeleteCartForm(FlaskForm):
    submit = SubmitField('Vaciar Carrito')