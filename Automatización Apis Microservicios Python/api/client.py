"""
Cliente API para automatización de pruebas.

Enfoque QA: Clase base reutilizable para todas las interacciones con APIs.
Proporciona métodos comunes (GET, POST, etc.) con logging y validaciones.
Permite mocking para pruebas unitarias.
"""

import requests
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import Config
from utils.helpers import log_request, validate_response

class APIClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or Config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)

    def get(self, endpoint, params=None, expected_status=200):
        """
        Realiza una petición GET.

        QA: Método estandarizado para consultas, con validación automática.
        """
        url = f"{self.base_url}{endpoint}"
        log_request('GET', url, params)
        response = self.session.get(url, params=params, timeout=Config.TIMEOUT)
        validate_response(response, expected_status)
        return response

    def post(self, endpoint, data=None, expected_status=201):
        """
        Realiza una petición POST.

        QA: Para crear recursos, con validación de datos enviados.
        """
        url = f"{self.base_url}{endpoint}"
        log_request('POST', url, data)
        response = self.session.post(url, json=data, timeout=Config.TIMEOUT)
        validate_response(response, expected_status)
        return response

    def put(self, endpoint, data=None, expected_status=200):
        """
        Realiza una petición PUT.

        QA: Para actualizar recursos existentes.
        """
        url = f"{self.base_url}{endpoint}"
        log_request('PUT', url, data)
        response = self.session.put(url, json=data, timeout=Config.TIMEOUT)
        validate_response(response, expected_status)
        return response

    def delete(self, endpoint, expected_status=204):
        """
        Realiza una petición DELETE.

        QA: Para eliminar recursos, verificando eliminación exitosa.
        """
        url = f"{self.base_url}{endpoint}"
        log_request('DELETE', url)
        response = self.session.delete(url, timeout=Config.TIMEOUT)
        validate_response(response, expected_status)
        return response