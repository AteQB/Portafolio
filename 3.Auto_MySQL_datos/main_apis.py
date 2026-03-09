# 1. IMPORTACIONES: Herramientas para la API y conexión a Base de Datos
from fastapi import FastAPI, Query
import mysql.connector
from typing import Optional

# 2. INICIALIZACIÓN: Creamos la instancia de FastAPI
app = FastAPI()

# 3. CONEXIÓN: Configuración para tu base de datos 'muestra_mineria'
# Se utiliza el usuario root y host local de tu XAMPP/Laragon
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="", 
        database="muestra_mineria"
    )

# 4. MÉTODO GET: Consulta con filtros para Minería de Datos
# IMPORTANTE: Los nombres de estas variables deben ser iguales en Postman (Key)
@app.get("/api/v1/buscar")
def filtrar_vehiculos(
    nombre: Optional[str] = None, 
    tipo: Optional[str] = None, 
    uso: Optional[str] = None
):
    # Abrimos la conexión y el cursor en formato diccionario para JSON
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Iniciamos la consulta base con el truco '1=1'
    query = "SELECT * FROM usuarios_prueba WHERE 1=1"
    valores = []

    # Lógica de filtrado dinámico:
    # Si el parámetro llega desde Postman, se agrega a la consulta SQL
    if nombre:
        query += " AND nombre LIKE %s"
        valores.append(f"%{nombre}%") # Búsqueda parcial (ej: 'Lucia' encuentra 'Lucia Castro')
        
    if tipo:
        # Filtra por columna 'tipo_vehiculo' usando el parámetro 'tipo'
        query += " AND tipo_vehiculo = %s"
        valores.append(tipo)
        
    if uso:
        # Filtra por columna 'tipo_uso' usando el parámetro 'uso'
        query += " AND tipo_uso = %s"
        valores.append(uso)

    # Ejecución de la consulta final filtrada
    cursor.execute(query, valores)
    resultados = cursor.fetchall()
    
    # Cierre de conexiones para liberar recursos del sistema
    cursor.close()
    conn.close() 
    
    # Retornamos los datos filtrados (si no hay filtros, devuelve los 50 registros)
    return resultados