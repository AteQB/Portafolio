# 1. IMPORTACIONES: Traemos las herramientas necesarias
# FastAPI: El motor para crear la API
# Optional: Permite que los filtros sean opcionales (puedes buscar por nombre o no)
from fastapi import FastAPI, Query
import mysql.connector
from typing import Optional

# 2. INICIALIZACIÓN: Creamos la aplicación
app = FastAPI()

# 3. CONEXIÓN: Función para conectar con tu base de datos MariaDB
# Usamos los datos que se ven en tu phpMyAdmin (127.0.0.1 y usuario root)
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="", # Por defecto en XAMPP está vacío
        database="muestra_mineria"
    )

# 4. MÉTODO GET (Consulta): La "puerta" para buscar datos desde Postman
# Definimos la ruta '/api/v1/buscar' y los parámetros de búsqueda
@app.get("/api/v1/buscar")
def filtrar_vehiculos(
    nombre: Optional[str] = None, 
    tipo: Optional[str] = None, 
    uso: Optional[str] = None
):
    # Abrimos la conexión y preparamos el cursor en formato diccionario
    # Esto es vital para que Postman reciba los datos como clave:valor (JSON)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # ESTRUCTURA DE LA CONSULTA SQL DINÁMICA:
    # 'WHERE 1=1' permite ir agregando filtros de forma flexible
    query = "SELECT * FROM usuarios_prueba WHERE 1=1"
    valores = []

    # Lógica de búsqueda: Si envías un dato en Postman, se agrega al SQL
    if nombre:
        query += " AND nombre LIKE %s"
        valores.append(f"%{nombre}%") # % permite coincidencias parciales
    if tipo:
        query += " AND tipo_vehiculo = %s"
        valores.append(tipo)
    if uso:
        query += " AND tipo_uso = %s"
        valores.append(uso)

    # Ejecutamos la consulta con los filtros aplicados
    cursor.execute(query, valores)
    resultados = cursor.fetchall()
    
    # Cerramos conexiones para liberar recursos del servidor
    cursor.close()
    conn.close()
    
    # Devolvemos los datos encontrados
    return resultados

# Para ejecutar la API, usa el siguiente comando en la terminal:
# uvicorn main_apis:app --reload