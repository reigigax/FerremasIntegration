from flask import Flask, render_template, jsonify, url_for, flash, redirect, request, session
from forms import TransactionForm
import requests

app = Flask(__name__)

#?Llave secreta para el funcionamiento de formularios
app.config['SECRET_KEY'] = '9b556bcc4473533428a56d86735ff7f9'

#?Direccion Pincipal API
api_base = "http://127.0.0.1:5001/"

#*APIs productos
api_obtener_productos = api_base + "api/obtener-productos"
api_obtener_producto_por_id = api_base + "api/obtener-producto-id/"

#*APIs carrito

#*API banco central
api_bancocentral_valor_dolar = api_base + "api/bancocentral/trimestre/ultimo-valor-dolar"

#*API transbank


#*Renderizacion de los templates
@app.route('/', methods=['POST', 'GET'])
@app.route('/test', methods=['POST', 'GET'])
def test():
    webpay_form = TransactionForm()

    get_request_products = requests.get(api_obtener_productos)
    json_products = get_request_products.json()

    get_request_value_dolar = requests.get(api_bancocentral_valor_dolar)
    json_dolar_value_bancocentral = get_request_value_dolar.json()

    if json_products and json_dolar_value_bancocentral:
        return render_template("test.html", products=json_products, dolar_value=json_dolar_value_bancocentral, form=webpay_form)
    else:
        return render_template("test.html")

#*Actualiza las modificaciones realizadas sin reiniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, port="5000")