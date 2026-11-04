from flask import Flask, jsonify, abort, request
import pymysql
import requests
from decimal import Decimal

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3307,
        user="clase",
        password="clase123",
        database="creditos",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }

@app.errorhandler(400)
def error_400(error):
    return jsonify({
        "error": {
            "codigo": 400,
            "mensaje": "Bad Request",
            "descripcion": "Los datos de entrada son incorrectos."
        }
    }), 400

@app.errorhandler(404)
def error_404(error):
    return jsonify({
        "error": {
            "codigo": 404,
            "mensaje": "Not Found",
            "descripcion": "El recurso solicitado no existe."
        }
    }), 404
    

@app.errorhandler(409)
def error_409(error):
    return jsonify({
        "error": {
            "codigo": 409,
            "mensaje": "Conflict",
            "descripcion": "La petición entra en conflicto con el estado actual del recurso."
        }
    }), 409
    

@app.errorhandler(415)
def error_415(error):
    return jsonify({
        "error" : {
            "codigo": 415,
            "mensaje": "Unsupported Media Type",
            "descripcion": "El formato de los datos recibidos no está soportado. Se esperaba JSON."
        }
    }), 415

@app.errorhandler(500)
def error_500(error):
    app.logger.error("Error interno del servidor: %s", error)
    return jsonify({
        "error": {
            "codigo": 500,
            "mensaje": "Internal Server Error",
            "descripcion": "Se ha producido un error inesperado en el servidor."
        }
    }), 500

@app.errorhandler(405)
def manejar_405(error):
    return jsonify({
        "error": {
            "code": 405,
            "message": "Método HTTP no permitido para esta ruta"}}), 405

@app.get("/clientes")
def obtener_clientes():
    conexion = get_connection()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM clientes_credito LIMIT 100")
        clientes = cursor.fetchall()
    conexion.close()
    return jsonify(clientes)

@app.get("/clientes/<id>")
def obtener_cliente(id):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE id = %s", (id,))
            cliente = cursor.fetchone()
    finally:
        conexion.close()
    if not cliente:
        abort(404, description=f"Cliente con ID {id} no encontrado")
    return jsonify(cliente), 200

@app.get("/clientes/impago")
def filtrar_por_impago():
    impago = request.args.get("impago", type=int)
    if impago is None or impago not in [0, 1]:
        abort(400, description="Se debe rellenar la variable 'impago' y debe ser 0 o 1")
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE Impago = %s", (impago,))
            clientes = cursor.fetchall()
    finally:
        conexion.close()
    return jsonify(clientes), 200

@app.get("/clientes/scoring")
def filtrar_por_scoring():
    scoring_min = request.args.get("min", type=int)
    scoring_max = request.args.get("max", type=int)
    query = "SELECT * FROM clientes_credito WHERE 1=1"
    params = []
    if scoring_min is not None:
        query += " AND Scoring_Crediticio >= %s"
        params.append(scoring_min)
    if scoring_max is not None:
        query += " AND Scoring_Crediticio <= %s"
        params.append(scoring_max)
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(query, tuple(params))
            clientes = cursor.fetchall()
    finally:
        conexion.close()
    return jsonify(clientes), 200

@app.get("/clientes/ingresos")
def filtrar_por_ingresos():
    ingresos_min = request.args.get("min", type=float)
    ingresos_max = request.args.get("max", type=float)
    query = "SELECT * FROM clientes_credito WHERE 1=1"
    params = []
    if ingresos_min is not None:
        query += " AND Ingresos >= %s"
        params.append(ingresos_min)
    if ingresos_max is not None:
        query += " AND Ingresos <= %s"
        params.append(ingresos_max)
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(query, tuple(params))
            clientes = cursor.fetchall()
    finally:
        conexion.close()
    return jsonify(clientes), 200

@app.get("/clientes/ratio-deuda-ingresos")
def filtrar_por_ratio_deuda_ingresos():
    ratio_max = request.args.get("max", type=float)
    if ratio_max is None:
        abort(400, description="Se requiere especificar el parámetro 'max'")
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE Ratio_Deuda_Ingresos <= %s", (ratio_max,))
            clientes = cursor.fetchall()
    finally:
        conexion.close()
    return jsonify(clientes), 200

@app.get("/clientes/proposito")
def filtrar_por_proposito():
    proposito = request.args.get("proposito", type=str)
    if not proposito:
        abort(400, description="Se tiene que especificar el parámetro 'proposito'")
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE Proposito = %s", (proposito,))
            clientes = cursor.fetchall()
    finally:
        conexion.close()
    return jsonify(clientes), 200

@app.get("/clientes/jornada")
def filtrar_por_jornada():
    tipo = request.args.get("tipo", type=str)
    if not tipo:
        abort(400, description="Se debe especificar el parámetro 'tipo'")
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE Tipo_Jornada_Laboral = %s", (tipo,))
            clientes = cursor.fetchall()
    finally:
        conexion.close()
    return jsonify(clientes), 200

@app.post("/clientes")
def crear_cliente():
    datos = request.get_json()
    if not datos:
        abort(400, description="LA petición debe ser un JSON válido")
    campos_obligatorios = ["ID", "Edad", "Ingresos", "Monto_Inicial", "Proposito"]
    for campo in campos_obligatorios:
        if campo not in datos:
            abort(400, description="Falta el campo obligatorio")
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO clientes_credito (
                    ID, Edad, Ingresos, Monto_Inicial, Proposito, Scoring_Crediticio, Meses_Empleo, Num_Creditos, 
                    Ratio_Interes, Duracion, Ratio_Deuda_Ingresos, Estudios, Tipo_Jornada_Laboral, Estado_Civil, 
                    Posesion_Hipoteca, Personas_Cargo, Fiador, Impago, Prima) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (datos["ID"], datos["Edad"], datos["Ingresos"], datos["Monto_Inicial"], datos["Proposito"],
                datos.get("Scoring_Crediticio"), datos.get("Meses_Empleo"), datos.get("Num_Creditos", 1),
                datos.get("Ratio_Interes"), datos.get("Duracion"), datos.get("Ratio_Deuda_Ingresos"),datos.get("Estudios"), 
                datos.get("Tipo_Jornada_Laboral"), datos.get("Estado_Civil"),datos.get("Posesion_Hipoteca", 0), 
                datos.get("Personas_Cargo", 0), datos.get("Fiador", 0), datos.get("Impago", 0), datos.get("Prima"))
            cursor.execute(sql, valores)
        conexion.commit()
    finally:
        conexion.close()
    return jsonify({"mensaje": "Cliente registrado correctamente", "cliente": datos}), 201

@app.patch("/clientes/<id>")
def modificar_cliente(id):
    datos = request.get_json()
    if not datos:
        abort(400, description="Los datos de la petición debe estar en formato JSON")
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE ID = %s", (id,))
            cliente = cursor.fetchone()
            if not cliente:
                abort(404, description="Cliente no encontrado")
            campos_sql = []
            valores = []
            for clave, valor in datos.items():
                campos_sql.append(f"{clave} = %s")
                valores.append(valor)
            valores.append(id)
            sql = f"UPDATE clientes_credito SET {', '.join(campos_sql)} WHERE ID = %s"
            cursor.execute(sql, tuple(valores))
        conexion.commit()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE ID = %s", (id,))
            cliente_actualizado = cursor.fetchone()
    finally:
        conexion.close()
    return jsonify(cliente_actualizado), 200

@app.delete("/clientes/<id>")
def eliminar_cliente(id):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito WHERE ID = %s", (id,))
            cliente = cursor.fetchone()
            if not cliente:
                abort(404, description=f"Cliente con ID '{id}' no encontrado")
            cursor.execute("DELETE FROM clientes_credito WHERE ID = %s", (id,))
        conexion.commit()
    finally:
        conexion.close()
    return jsonify({"mensaje": f"Cliente con ID '{id}' eliminado correctamente"}), 200

@app.get("/pais/<string:nombre>")
def obtener_info_pais(nombre):
    url = f"https://restcountries.com/v3.1/name/{nombre}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            abort(400, description=f"País '{nombre}' no encontrado")
        response.raise_for_status()
        datos_pais = response.json()
    except requests.RequestException:
        abort(500, description="Error al conectar con el servicio externo REST Countries")
    pais = datos_pais[0]
    resultado = {
        "nombre_comun": pais.get("name", {}).get("common"),"nombre_oficial": pais.get("name", {}).get("official"),
        "capital": pais.get("capital", ["No disponible"])[0], "region": pais.get("region"),"poblacion": pais.get("population"),
        "monedas": pais.get("currencies"),"bandera": pais.get("flags", {}).get("png")}
    return jsonify(resultado), 200

def convertir_decimales(filas):
    for fila in filas:
        for clave, valor in fila.items():
            if isinstance(valor, Decimal):
                fila[clave] = float(valor)
    return filas

@app.get("/powerbi/clientes")
def clientes_powerbi():
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes_credito")
            clientes = cursor.fetchall()
    finally:
        conexion.close()
    return jsonify(convertir_decimales(clientes)), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)