"""
Configuración para el framework de automatización de APIs.

Enfoque QA: Centralizar configuraciones para facilitar mantenimiento y reutilización.
Permite cambiar entornos (desarrollo, staging, producción) sin modificar código.
"""

import os

class Config:
    BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')  # URL base de la API
    TIMEOUT = int(os.getenv('API_TIMEOUT', 10))  # Timeout en segundos
    HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Configuraciones de QA
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    REPORT_DIR = os.getenv('REPORT_DIR', 'reports/')