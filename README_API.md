
Este proyecto proporciona un entorno Docker con una base de datos MySQL ya preparada y cargada a partir de los datos disponibles en `datos/datos.xlsx`.

La base de datos utiliza almacenamiento persistente mediante un volumen Docker.

## Arranque

```bash
docker compose up --build
```

Servicios disponibles:

* API Flask: `http://localhost:8000`
* MySQL: `localhost:3306`
* Base de datos: `creditos`
* Usuario: `clase`
* Contraseña: `clase123`
* Tabla: `clientes_credito`

## Estructura

```text
.
├── api/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── datos/
│   └── datos.xlsx
│
├── loader/
│   ├── Dockerfile
│   ├── load_data.py
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

El trabajo sobre la API se realizará principalmente en:

```text
api/main.py
```

## Persistencia

Los datos de MySQL se almacenan en un volumen Docker y se mantienen aunque se detengan los contenedores:

```bash
docker compose down
```

Para volver a levantar el entorno:

```bash
docker compose up
```

Si se elimina el volumen:

```bash
docker compose down -v
```

la base de datos se volverá a generar a partir del fichero de datos en el siguiente arranque.

# Endpoints

# / (get)
```json
{
"/":
	"get": 
		"summary": "mensaje": "API funcionando"
		"Description": "Comprobacion del funcionamiento de la API"
    "RequestBody": "No"
    "Parameters": "No"
    "responses":
        200:
        "description": "API operativa"
        "content":
          "Aplication/json":
            "schema":
              "type": "object"
              "properties":
                "mensaje":
                  "type": "string"
                  "example": "API funcionando"}
```
# / (clientes)

```json
{
"/":
  "clientes":
  "get":
    "summary": "Obtener clientes"
    "Description": "Consulta y devuelve un listado de clientes de la base de datos"
    "RequestBody": "No"
    "Parameters": "No"
    "responses":
        200:
        "description": "Listado de clientes obtenido correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"}
```

# / (clientes) / ID
```json
{
"/clientes/<id>":
  "get":
    "summary": "Obtener cliente por ID"
    "Description": "Consulta un cliente especifico de la base de datos mediante su ID"
    "RequestBody": "No"
    "Parameters":
      "id":
        "type": "string"
        "in": "path"
        "required": "true"
    "responses":
        200:
        "description": "Cliente encontrado correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "object"
        404:
        "description": "Cliente no encontrado"}
```

# / (clientes) / (impago)
```json
{
"/clientes/impago":
  "get":
    "summary": "Filtrar clientes por impago"
    "Description": "Filtra y devuelve la lista de clientes segun su estado de impago (0 o 1)"
    "RequestBody": "No"
    "Parameters":
      "impago":
        "type": "integer"
        "in": "query"
        "required": "true"
    "responses":
        200:
        "description": "Clientes filtrados obtenidos correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"
        400:
        "description": "El parametro impago no es valido o no ha sido proporcionado"}
```

# / (clientes) / (scoring)
```json
{
"/clientes/scoring":
  "get":
    "summary": "Filtrar clientes por scoring crediticio"
    "Description": "Filtra y devuelve la lista de clientes en base a un rango minimo y/o maximo de scoring crediticio"
    "RequestBody": "No"
    "Parameters":
      "min":
        "type": "integer"
        "in": "query"
        "required": "false"
      "max":
        "type": "integer"
        "in": "query"
        "required": "false"
    "responses":
        200:
        "description": "Clientes filtrados por scoring obtenidos correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"}
```

# / (clientes) / (ingresos)
```json
{
"/clientes/ingresos":
  "get":
    "summary": "Filtrar clientes por ingresos"
    "Description": "Filtra y devuelve la lista de clientes en base a un rango minimo y/o maximo de ingresos"
    "RequestBody": "No"
    "Parameters":
      "min":
        "type": "number"
        "in": "query"
        "required": "false"
      "max":
        "type": "number"
        "in": "query"
        "required": "false"
    "responses":
        200:
        "description": "Clientes filtrados por ingresos obtenidos correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"}
```

# / (clientes) / (ratio-deuda-ingresos)
```json
{
"/clientes/ratio-deuda-ingresos":
  "get":
    "summary": "Filtrar clientes por ratio deuda/ingresos"
    "Description": "Filtra y devuelve la lista de clientes cuyo ratio deuda/ingresos es menor o igual al valor maximo indicado"
    "RequestBody": "No"
    "Parameters":
      "max":
        "type": "number"
        "in": "query"
        "required": "true"
    "responses":
        200:
        "description": "Clientes filtrados por ratio deuda/ingresos obtenidos correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"
        400:
        "description": "Se requiere especificar el parametro max"}
```

# / (clientes) / (proposito)
```json
{
"/clientes/proposito":
  "get":
    "summary": "Filtrar clientes por propósito"
    "Description": "Filtra y devuelve la lista de clientes según el propósito específico del crédito"
    "RequestBody": "No"
    "Parameters":
      "proposito":
        "type": "string"
        "in": "query"
        "required": "true"
    "responses":
        200:
        "description": "Clientes filtrados por propósito obtenidos correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"
        400:
        "description": "Se tiene que especificar el parámetro propósito"}
```

# / (clientes) / (jornada)
```json
{
"/clientes/jornada":
  "get":
    "summary": "Filtrar clientes por jornada laboral"
    "Description": "Filtra y devuelve la lista de clientes según su tipo de jornada laboral"
    "RequestBody": "No"
    "Parameters":
      "tipo":
        "type": "string"
        "in": "query"
        "required": "true"
    "responses":
        200:
        "description": "Clientes filtrados por tipo de jornada obtenidos correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"
        400:
        "description": "Se debe especificar el parámetro tipo"}
```

# / (clientes)
```json
{
"/clientes":
  "post":
    "summary": "Crear cliente"
    "Description": "Registra un nuevo cliente en la base de datos validando los campos obligatorios"
    "RequestBody":
      "schema":
        "type": "object"
        "required":
          - "ID"
          - "Edad"
          - "Ingresos"
          - "Monto_Inicial"
          - "Proposito"
        "properties":
          "ID":
            "type": "string"
          "Edad":
            "type": "integer"
          "Ingresos":
            "type": "number"
          "Monto_Inicial":
            "type": "number"
          "Proposito":
            "type": "string"
    "Parameters": "No"
    "responses":
        201:
        "description": "Cliente registrado correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "object"
              "properties":
                "mensaje":
                  "type": "string"
                  "example": "Cliente registrado correctamente"
                "cliente":
                  "type": "object"
        400:
        "description": "La petición debe ser un JSON válido o falta algún campo obligatorio"}
```

# / (clientes) / id
```json
{
"/clientes/<id>":
  "patch":
    "summary": "Modificar cliente"
    "Description": "Actualiza parcialmente los datos de un cliente existente identificado por su ID"
    "RequestBody":
      "schema":
        "type": "object"
    "Parameters":
      "id":
        "type": "string"
        "in": "path"
        "required": "true"
    "responses":
        200:
        "description": "Cliente actualizado correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "object"
        400:
        "description": "Los datos de la petición debe estar en formato JSON"
        404:
        "description": "Cliente no encontrado"}
```

# / (clientes) / id 
```json
{
"/clientes/<id>":
  "delete":
    "summary": "Eliminar cliente"
    "Description": "Elimina un registro de cliente de la base de datos mediante su ID"
    "RequestBody": "No"
    "Parameters":
      "id":
        "type": "string"
        "in": "path"
        "required": "true"
    "responses":
        200:
        "description": "Cliente eliminado correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "object"
              "properties":
                "mensaje":
                  "type": "string"
                  "example": "Cliente con ID 'CLI999' eliminado correctamente"
        404:
        "description": "Cliente no encontrado"}
```

# / (pais)
```json
{
"/pais/<string:nombre>":
  "get":
    "summary": "Obtener información de un país"
    "Description": "Consulta la API externa REST Countries para obtener información geográfica y demográfica de un país según su nombre"
    "RequestBody": "No"
    "Parameters":
      "nombre":
        "type": "string"
        "in": "path"
        "required": "true"
    "responses":
        200:
        "description": "Información del país obtenida correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "object"
              "properties":
                "nombre_comun":
                  "type": "string"
                "nombre_oficial":
                  "type": "string"
                "capital":
                  "type": "string"
                "region":
                  "type": "string"
                "poblacion":
                  "type": "integer"
                "monedas":
                  "type": "object"
                "bandera":
                  "type": "string"
        400:
        "description": "País no encontrado"
        500:
        "description": "Error al conectar con el servicio externo REST Countries"}
```

# Deteccion de errores

# Error 400 
```json
{
    "error": {
        "code": 400,
        "message": "Los datos de entrada son incorrectos"
    }
}
```

# Error 404 
```json
{
    "error": {
        "code": 404,
        "message": "El recurso solicitado no existe"
    }
}
```

# Error 409 
```json
{
    "error": {
        "code": 409,
        "message": "La petición entra en conflicto con el estado actual del recurso"
    }
}
```

# Error 415 
```json
{
    "error": {
        "code": 415,
        "message": "El formato de los datos recibidos no está soportado. Se esperaba JSON"
    }
}
```

# Error 500 
```json
{
    "error": {
        "code": 500,
        "message": "Se ha producido un error inesperado en el servidor"
    }
}
```

# Error 405 
```json
{
    "error": {
        "code": 405,
        "message": "Método HTTP no permitido para esta ruta"
    }
}
``` 

```json
{
"convertir_decimales(filas)":
  "function":
    "summary": "Convertir objetos Decimal a float"
    "Description": "Recorre una lista de diccionarios (filas) y convierte cualquier valor de tipo Decimal a float para permitir su correcta serializacion a JSON"
    "RequestBody": "No"
    "Parameters":
      "filas":
        "type": "array"
        "in": "argument"
        "required": "true"
        "description": "Lista de diccionarios devuelta por la base de datos"
    "returns":
        "description": "Lista de diccionarios con los valores Decimal transformados a float"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"
}
```

```json
{
"/powerbi/clientes":
  "get":
    "summary": "Obtener todos los clientes para Power BI"
    "Description": "Consulta y devuelve la totalidad de los registros de clientes sin límite, aplicando la conversión de tipos Decimal a float para su integración con Power BI"
    "RequestBody": "No"
    "Parameters": "No"
    "responses":
        200:
        "description": "Listado completo de clientes obtenido y procesado correctamente"
        "content":
          "Aplication/json":
            "schema":
              "type": "array"
              "items":
                "type": "object"
}
```