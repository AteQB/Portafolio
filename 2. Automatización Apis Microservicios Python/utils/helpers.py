"""
Utilidades auxiliares para el framework de automatización.

Enfoque QA: Funciones reutilizables para validaciones, logging y manejo de datos.
Ayudan a mantener consistencia en las pruebas y reducir código duplicado.
"""

import json
import logging
from .config import Config

# Configurar logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

def load_json_data(file_path):
    """
    Carga datos desde un archivo JSON.

    QA: Facilita la separación de datos de prueba del código, permitiendo
    actualizaciones sin modificar lógica de pruebas.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error al parsear JSON: {e}")
        return {}

def validate_response(response, expected_status=200):
    """
    Valida respuesta HTTP básica.

    QA: Verificación estándar de respuestas para asegurar consistencia
    en todas las pruebas funcionales.
    """
    assert response.status_code == expected_status, f"Status esperado {expected_status}, obtenido {response.status_code}"
    logger.info(f"Respuesta válida: {response.status_code}")

def log_request(method, url, data=None):
    """
    Registra detalles de una petición HTTP.

    QA: Mejora trazabilidad de pruebas, facilitando debugging y reporting.
    """
    logger.info(f"Petición: {method} {url}")
    if data:
        logger.debug(f"Datos enviados: {data}")