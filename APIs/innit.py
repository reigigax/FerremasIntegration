from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
import requests

#? Imports de Transbank
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType

#? Configuracion de Conexion a BD mediante una clase
from db_settings import db_settings

app = Flask(__name__)

#? Creacion de la conexion a Base de Datos
conn = MySQL(app)

#? Esto permite solicitudes desde cualquier origen
CORS(app)

#? Url Raiz de las APIs
url_base="http://127.0.0.1:5001"

#* API Obtencion de Productos [GET]
@app.route("/api/obtener-productos", methods=["GET"])
def get_products():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT id_producto, codigo_producto, marca_producto, nombre_producto, categoria_producto, stock, sucursal, valor, descripcion, img_producto FROM productos"
        cursor.execute(sql)
        data = cursor.fetchall()
        products = []
        
        for row in data:
            product = {'id_producto':row[0], 'codigo_producto':row[1], 'marca_producto':row[2], 'nombre_producto':row[3], 'categoria_producto':row[4], 'stock':row[5], 'sucursal':row[6], 'valor':row[7], 'descripcion':row[8], 'img_producto':row[9]}
            products.append(product)
        
        return jsonify({'productos':products, 'mensaje':'Productos Obtenidos'})
    except Exception as ex:
        return jsonify({'mensaje_error':'Productos no Encontrados','descripcion_error':f"Error: {str(ex)}"})

#* API Filtro de Productos por sucursal [GET]
@app.route('/api/obtener-productos/sucursal/<sucursal>', methods=["GET"])
def filtro_productos_sucursal(sucursal):
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT id_producto, codigo_producto, marca_producto, nombre_producto, categoria_producto, stock, sucursal, valor FROM productos WHERE sucursal = '{0}'".format(sucursal)
        cursor.execute(sql)
        data = cursor.fetchone()
        products = []

        if data != None:
            product = {'id_producto':data[0], 'codigo_producto':data[1], 'marca_producto':data[2], 'nombre_producto':data[3], 'categoria_producto':data[4], 'stock':data[5], 'sucursal':data[6], 'valor':data[7]}
            products.append(product)
            return jsonify({'producto':products, 'mensaje':'Productos Encontrado'})
        else:
            return jsonify({'mensaje','Productos no Encontrados o No Disponibles en Sucursal'})
    except Exception as ex:
        return jsonify({'mensaje_error':'Productos no Encontrados','descripcion_error':f"Error: {str(ex)}"})

#* API Obtencion de Productos por Codigo Producto [GET]
@app.route("/api/obtener-producto-id/<id_product>", methods=["GET"])
def get_product_by_id(id_product):
    try:
        #* Lectura y Obtencion del JSON
        #data_request_post = request.get_json()
        #id_product = data_request_post["id_product"]

        cursor = conn.connection.cursor()
        sql = "SELECT id_producto, codigo_producto, marca_producto, nombre_producto, categoria_producto, stock, sucursal, valor FROM productos WHERE id_producto = '{0}'".format(id_product)
        cursor.execute(sql)
        data = cursor.fetchone()
        product = {}

        if data != None:
            product = {'id_producto':data[0], 'codigo_producto':data[1], 'marca_producto':data[2], 'nombre_producto':data[3], 'categoria_producto':data[4], 'stock':data[5], 'sucursal':data[6], 'valor':data[7]}
            return jsonify({'producto':product, 'mensaje':'Producto Encontrado'})
        else:
            return jsonify({'mensaje','Producto no Encontrado o Fuera de Stock'})
    except Exception as ex:
        return jsonify({'mensaje_error':'Producto no Encontrado','descripcion_error':f"Error: {str(ex)}"})

#* API Obtencion del Valor del Dolar en el ultimo Trimestre [GET]
@app.route("/api/bancocentral/trimestre/ultimo-valor-dolar", methods=["GET"])
def get_dolar_value():
    try:        
        #Formato YYYY-MM-DD
        fecha_actual_sistema = datetime.now()
        fecha_formato = fecha_actual_sistema.strftime('%Y-%m-%d')
        fecha_actual = fecha_formato

        anio_actual_sistema = int(fecha_actual_sistema.strftime('%Y'))
        mes_actual_sistema = int(fecha_actual_sistema.strftime('%m'))
        dia_actual_sistema = 1
        
        if mes_actual_sistema == 2 or mes_actual_sistema == 1:
            mes_actual_sistema -= 2
            anio_actual_sistema -= 1
            if mes_actual_sistema == 0:
                mes_actual_sistema = 12
            if mes_actual_sistema == -1:
                mes_actual_sistema = 11
        else:
            mes_actual_sistema = mes_actual_sistema-2

        if mes_actual_sistema <= 9:
            mes_actual_sistema = f"0{mes_actual_sistema}"

        fecha_trimesre = f"{anio_actual_sistema}-{mes_actual_sistema}-0{dia_actual_sistema}"

        #Parametros para consulta de la Api del Banco Central 
        api_bancocentral_ruta = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?"
        api_bancocentral_usuario = "user=ren.gonzalezp@duocuc.cl&"
        api_bancocentral_contrasena = "pass=Lol879pop&"
        api_bancocentral_fecha_inicio = "firstdate="+fecha_trimesre+"&"
        api_bancocentral_fecha_actual = "lastdate="+fecha_actual+"&"
        api_bancocentral_serie = "timeseries=F073.TCO.PRE.Z.D&"
        api_bancocentral_funcion ="function=GetSeries"

        #Consulta a la API
        api_bancocentral_consulta_completa = api_bancocentral_ruta+api_bancocentral_usuario+api_bancocentral_contrasena+api_bancocentral_fecha_inicio+api_bancocentral_fecha_actual+api_bancocentral_serie+api_bancocentral_funcion

        #Respuesta de API en formato JSON
        respuesta_api_bancocentral = requests.get(api_bancocentral_consulta_completa)
        data_banco_central = respuesta_api_bancocentral.json()
        #Se filtra la Respuesta para Obtener los datos de el Array "Obs"
        data_valor_dolar = data_banco_central["Series"]["Obs"]

        #Se verifica si existen datos dentro del Array
        if data_valor_dolar:
            #Filtro de Fechas donde presenten el Valor del Dolar
            valores_dolar_notnull = []
            for item in data_valor_dolar:
                if item["statusCode"] == "OK":
                    valores_dolar_notnull.append(item)
            #Flito de Fechas posteriores a la Fecha Actual
            valores_dolar_notnull_fechas_anteriores = []
            for item in valores_dolar_notnull:
                if item["indexDateString"] <= fecha_actual:
                    valores_dolar_notnull_fechas_anteriores.append(item)
            #Seleccion de la Ultima Fecha con Valor del Dolar despues del Filtrado
            ultimo_valor_dolar = {}
            if valores_dolar_notnull_fechas_anteriores:
                ultimo_valor_dolar = valores_dolar_notnull_fechas_anteriores[-1]
        else:
            val_dolar="No Hay Registros del Dolar Disponibles"

        informacion_valdolar = ultimo_valor_dolar
        val_dolar=float(ultimo_valor_dolar["value"])

        return jsonify({'Fecha Actual en Chile': fecha_actual, 'mensaje':'success', 'Valor Dolar':val_dolar, 'Info API Banco Central':informacion_valdolar,"Fecha Inicio Trimestre":fecha_trimesre})
    except Exception as ex:
        return jsonify({'mensaje':'Error al Intentar Obtener el Valor del Dolar', 'descripcion_error':f"Error: {str(ex)}"})

#* API Obtencion de link para Transaccion en WebPay-Transbank [POST]
@app.route('/api/transaccion-webpay', methods=['POST'])
def realizar_pago():
    try:
        url_compra_finalizada = "http://127.0.0.1:5000"

        transaction_info = request.get_json()
        orden_compra = transaction_info['orden_compra']
        id_session = transaction_info['sesion']
        monto = transaction_info['monto']
        redirect_url = url_compra_finalizada

        execute_transaction = Transaction(options=WebpayOptions(commerce_code="597055555532", api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C", integration_type= IntegrationType.TEST, timeout=600))
        webpay_transaction = execute_transaction.create(buy_order=orden_compra, session_id=id_session, amount=monto, return_url=redirect_url)

        return jsonify({'url':webpay_transaction['url'], 'token':webpay_transaction['token']})
    except Exception as ex:
        return jsonify({'mensaje':'Error al contactar con WebPay', 'descripcion_error':f"Error: {str(ex)}"})

#* API Añadir Producto al Carrito [POST] [PUT]
@app.route('/api/carrito/agregar-producto/<id_producto>', methods=['POST', 'PUT'])
def agregar_producto_carrito(id_producto):
    try:
        data_request_post = request.get_json()
        quantity_product = data_request_post["cantidad"]
        quantity_product = int(quantity_product)
        
        api_producto_in_carrito = url_base + f"/api/carrito/producto/{id_producto}"
        respuesta_api_producto_in_carrito = requests.get(api_producto_in_carrito)
        producto_in_carrito = respuesta_api_producto_in_carrito.json()

        api_get_product = f"http://127.0.0.1:5001/api/obtener-producto-id/{id_producto}"
        product = requests.get(api_get_product)
        data_product = product.json()
        
        if quantity_product <= 0:
            return jsonify({"mensaje":"Cantidad para Agregar debe de ser mayor o igual a 1"})

        api_get_producto = url_base + f"/api/obtener-producto-id/{id_producto}"
        request_api_get_producto = requests.get(api_get_producto)
        stock_producto = request_api_get_producto.json()["producto"]["stock"]
        stock_producto = int(stock_producto)

        if quantity_product > stock_producto:
            return jsonify({"mensaje":f"Cantidad ingresada supera el Stock Actual del Producto ({stock_producto})"})

        if producto_in_carrito["mensaje"] == "Producto no se encuentra en el Carrito":
            if 'producto' not in data_product:
                return jsonify({"error": "Producto no encontrado"}), 404
            
            cursor = conn.connection.cursor()
            sql = "INSERT INTO carrito (id_producto, cantidad_producto) VALUES({0},{1})".format(data_product["producto"]["id_producto"], quantity_product)
            cursor.execute(sql)
            conn.connection.commit()

            return jsonify({"mensaje":"Producto Agregado Satisfactoriamente al Carrito"})
        else:
            cantidad_actual = producto_in_carrito["producto_carrito"]["cantidad_producto"]
            cantidad_total = cantidad_actual + quantity_product

            cursor = conn.connection.cursor()
            sql = f"UPDATE carrito SET cantidad_producto = {cantidad_total} WHERE id_producto = {id_producto}"
            cursor.execute(sql)
            conn.connection.commit()

            return jsonify({"mensaje":"Producto Agregado Satisfactoriamente al Carrito"})
    except Exception as ex:
        return jsonify({'mensaje':'Error al Agregar Producto al Carrito', 'descripcion_error':f"Error: {str(ex)}"})

#* API Obtener Productos del Carrito [GET]
@app.route('/api/carrito', methods=['GET'])
def obtener_productos_carrito():
    try:
        cursor = conn.connection.cursor()
        sql = "SELECT c.id_producto, p.codigo_producto, p.marca_producto, p.nombre_producto, p.categoria_producto, p.sucursal, p.valor, p.stock, p.descripcion, p.img_producto, SUM(c.cantidad_producto) FROM carrito c INNER JOIN productos p ON c.id_producto = p.id_producto GROUP BY id_producto"
        cursor.execute(sql)
        data = cursor.fetchall()
        productos_carrito = []

        if data:
            for row in data:
                product = {'id_producto':row[0], 'codigo_producto':row[1], 'marca_producto':row[2], 'nombre_producto':row[3], 'categoria_producto':row[4], 'sucursal':row[5], 'valor':row[6], 'stock':row[7], 'descripcion':row[8], 'img_producto':row[9],'cantidad_producto':row[10]}
                productos_carrito.append(product)
        else:
            return jsonify({"mensaje":"Carrito Vacio"})

        return jsonify({"mensaje":"Carrito Encontrado", "productos_carrito":productos_carrito})
    except Exception as ex:
        return jsonify({'mensaje':'Error al Agregar Producto al Carrito', 'descripcion_error':f"Error: {str(ex)}"})

#* API Obtener Productos del Carrito por Id [GET]
@app.route('/api/carrito/producto/<id_producto>', methods=["GET"])
def obtener_producto_porid_carrito_(id_producto):
    try:
        cursor = conn.connect.cursor()
        sql = "SELECT id_producto, cantidad_producto FROM carrito WHERE id_producto = {0}".format(id_producto)
        cursor.execute(sql)
        data = cursor.fetchone()
        producto_carrito={}

        if data:
            producto_carrito = {"id_producto":data[0],"cantidad_producto":data[1]}
            return jsonify({"mensaje":"Producto en Carrito Encontrado", "producto_carrito":producto_carrito})
        else:
            return jsonify({"mensaje":"Producto no se encuentra en el Carrito"})
    except Exception as ex:
        return jsonify({'mensaje':'Error al Bucar Productos en el Carrito', 'descripcion_error':f"Error: {str(ex)}"})

#* API Eliminar Producto del Carrito por Id [DELETE]
@app.route('/api/carrito/eliminar-producto/<id_producto>', methods=['DELETE'])
def eliminar_producto_carrito(id_producto):
    try:
        api_carrito = url_base + "/api/carrito"
        carrito = requests.get(api_carrito)
        productos = carrito.json()
        items = []

        for product in productos["productos_carrito"]:
            items.append(product["id_producto"])

        if int(id_producto) in items:
            cursor = conn.connection.cursor()
            sql = f"DELETE from carrito WHERE id_producto = {id_producto}"
            cursor.execute(sql)
            conn.connection.commit()

            return jsonify({"mensaje":"Producto Eliminado"})
        else:
            return jsonify({"mensaje":"Producto no se Encuentra Registrado en el Carrito"}),404
    except Exception as ex:
        return jsonify({'mensaje':'Error al Vaciar el Carrito', 'descripcion_error':f"Error: {str(ex)}"})
    
#* API Actualizar Cantidad de un Producto del Carrito [PUT]
@app.route('/api/carrito/modificar-producto/<id_producto>', methods=["PUT"])
def modificar_producto_carrito(id_producto):
    try:
        api_producto_en_carrito = url_base + f'/api/carrito/producto/{id_producto}'
        request_api_producto_en_carrito = requests.get(api_producto_en_carrito)
        producto_en_carrito = request_api_producto_en_carrito.json()

        data = request.get_json()
        nueva_cantidad = data.get("cantidad")

        if not nueva_cantidad or not isinstance(nueva_cantidad, int) or nueva_cantidad <= 0:
            return jsonify({"mensaje":"Cantidad Invalida"})
        
        if producto_en_carrito["mensaje"] == "Producto no se encuentra en el Carrito":
            return jsonify({"mensaje":"Producto No existe en Carrito"})

        api_get_producto = url_base + f"/api/obtener-producto-id/{id_producto}"
        request_api_get_producto = requests.get(api_get_producto)
        stock_producto = request_api_get_producto.json()["producto"]["stock"]
        stock_producto = int(stock_producto)

        if nueva_cantidad > stock_producto:
            return jsonify({"mensaje":f"Cantidad ingresada supera el Stock Actual del Producto ({stock_producto})"})

        cursor = conn.connection.cursor()
        sql = f"UPDATE carrito SET cantidad_producto = {nueva_cantidad} WHERE id_producto = {id_producto}"
        cursor.execute(sql)
        conn.connection.commit()

        return jsonify({"mensaje":"Cantidad del Producto Modificado"})
    except Exception as ex:
        return jsonify({'mensaje':'Error al Actualizar el Producto', 'descripcion_error':f"Error: {str(ex)}"})

#* API Vaciar Carrito [DELETE]
@app.route('/api/carrito/vaciar', methods=['DELETE'])
def vaciar_carrito():
    try:
        cursor = conn.connection.cursor()
        sql = "TRUNCATE TABLE carrito"
        cursor.execute(sql)
        conn.connect.commit()

        return jsonify({"mensaje":"Carrito Vaciado"})
    except Exception as ex:
        return jsonify({'mensaje':'Error al Vaciar el Carrito', 'descripcion_error':f"Error: {str(ex)}"})

#! Pagina de Error API
def page_not_found(error):
    return '<h1>La pagína que haces referencia no fue encontrada o no existe ...</h1>', 404

if __name__ == '__main__':
    app.config.from_object(db_settings['development'])
    app.register_error_handler(404, page_not_found)
    app.run(port="5001")