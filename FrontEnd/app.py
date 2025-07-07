from flask import Flask, render_template, jsonify, url_for, flash, redirect, request, session
from forms import TransactionForm, AddProductToCartForm, DeleteCartForm, DeleteProductFromCartForm, ModifyProductOnCartForm
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
api_obtener_carrito = api_base + "api/carrito"

#*API banco central
api_bancocentral_valor_dolar = api_base + "api/bancocentral/trimestre/ultimo-valor-dolar"

#*Renderizacion de los templates
@app.route('/home', methods=['POST', 'GET'])
def home():
    add_product_to_cart_form = AddProductToCartForm()

    get_request_products = requests.get(api_obtener_productos)
    json_products = get_request_products.json()

    get_carrito = requests.get(api_obtener_carrito)
    json_carrito = get_carrito.json()

    if json_products:
        if json_carrito:
            carrito_length = 0
            if json_carrito["mensaje"] == "Carrito Encontrado":
                for producto in json_carrito["productos_carrito"]:
                    carrito_length = carrito_length + 1
            else:
                carrito_length = 0
        return render_template("home.html", carrito_add_form= add_product_to_cart_form, products=json_products, carrito_length=carrito_length)
    else:
        return render_template("home.html")


@app.route('/carrito', methods=['POST', 'GET'])
def carrito():
    webpay_form = TransactionForm()
    delete_carrito_form = DeleteCartForm()
    carrito_delete_product_form = DeleteProductFromCartForm()
    carrito_modificar_producto_form = ModifyProductOnCartForm()

    sesion = app.secret_key
    subtotal = 0
    carrito_length = 0

    get_carrito = requests.get(api_obtener_carrito)
    json_carrito = get_carrito.json()

    if json_carrito:
        if json_carrito["mensaje"] == "Carrito Encontrado":
            for producto in json_carrito["productos_carrito"]:
                subtotal = subtotal + float(producto["valor"])*float(producto["cantidad_producto"])
                carrito_length = carrito_length + 1
        else:
            carrito_length = 0
        return render_template("carrito.html", carrito=json_carrito, carrito_delete_product=carrito_delete_product_form, carrito_delete_form=delete_carrito_form, carrito_modificar_producto=carrito_modificar_producto_form, form=webpay_form, sesion=sesion, carrito_length=carrito_length, subtotal=subtotal)
    else:
        return render_template("carrito.html")


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    get_carrito = requests.get(api_obtener_carrito)
    json_carrito = get_carrito.json()

    if json_carrito:
        carrito_length = 0
        if json_carrito["mensaje"] == "Carrito Encontrado":
            print(json_carrito["productos_carrito"])
            for producto in json_carrito["productos_carrito"]:
                carrito_length = carrito_length + 1
        else:
            carrito_length = 0

    if request.method == 'POST':
        # lógica de formulario
        pass
    return render_template('contacto.html', carrito_length=carrito_length)


@app.route('/catalogo')
def catalogo():
    get_carrito = requests.get(api_obtener_carrito)
    json_carrito = get_carrito.json()

    if json_carrito:
        carrito_length = 0
        if json_carrito["mensaje"] == "Carrito Encontrado":
            print(json_carrito["productos_carrito"])
            for producto in json_carrito["productos_carrito"]:
                carrito_length = carrito_length + 1
        else:
            carrito_length = 0

    try:
        response = requests.get(api_obtener_productos)
        data = response.json()  # Solo necesitas hacerlo una vez

        return render_template('catalogo.html', products=data, carrito_length=carrito_length)  # data es un dict con clave 'productos'

    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return render_template('catalogo.html', products={"productos": []})


#?Ruta de Pruebas
@app.route('/', methods=['POST', 'GET'])
@app.route('/test', methods=['POST', 'GET'])
def test():
    webpay_form = TransactionForm()
    carrito_add_form = AddProductToCartForm()
    carrito_delete_form = DeleteCartForm()
    carrito_delete_product = DeleteProductFromCartForm()
    carrito_modificar_producto = ModifyProductOnCartForm()

    get_request_products = requests.get(api_obtener_productos)
    json_products = get_request_products.json()

    get_request_value_dolar = requests.get(api_bancocentral_valor_dolar)
    json_dolar_value_bancocentral = get_request_value_dolar.json()

    get_carrito = requests.get(api_obtener_carrito)
    json_carrito = get_carrito.json()

    if json_products and json_dolar_value_bancocentral:
        return render_template("test.html", products=json_products, dolar_value=json_dolar_value_bancocentral, form=webpay_form, carrito_add_form=carrito_add_form, carrito_delete_product=carrito_delete_product, carrito_delete_form=carrito_delete_form, carrito_modificar_producto=carrito_modificar_producto, carrito=json_carrito)
    else:
        return render_template("test.html")

#? Ruta de Componentes
@app.route('/components/layout')
def navbar():
    get_carrito = requests.get(api_obtener_carrito)
    json_carrito = get_carrito.json()
    carrito_length = 0

    if json_carrito:
        for producto in json_carrito["productos_carrito"]:
            carrito_length =+ 1

        return render_template("components/layout.html", carrito_length=carrito_length)
    else:
        return render_template("components/layout.html")

#*Actualiza las modificaciones realizadas sin reiniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, port="5000")