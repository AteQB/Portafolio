"""
Casos de prueba funcionales para la API.

Enfoque QA: Pruebas que cubren escenarios funcionales completos.
Validan creación, lectura, actualización y eliminación de recursos.
Incluyen aserciones detalladas y manejo de datos de prueba.
"""

import pytest
import sys
import os

# Agregar el directorio raíz al path para imports absolutos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.client import APIClient
from api.endpoints import Endpoints
from utils.helpers import load_json_data
from utils.config import Config

class TestAPI:
    @pytest.fixture
    def client(self):
        """Fixture para cliente API.

        QA: Proporciona instancia fresca del cliente para cada prueba,
        asegurando aislamiento.
        """
        return APIClient()

    @pytest.fixture
    def test_data(self):
        """Fixture para datos de prueba.

        QA: Carga datos desde archivo externo, permitiendo variaciones
        sin cambiar código de pruebas.
        """
        return load_json_data('data/test_data.json')

    def test_get_users(self, client):
        """Prueba funcional: Obtener lista de usuarios.

        QA: Verifica que la API retorne usuarios existentes correctamente.
        """
        response = client.get(Endpoints.USERS)
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) > 0

    def test_create_user(self, client, test_data):
        """Prueba funcional: Crear nuevo usuario.

        QA: Valida creación de recursos con datos válidos.
        Verifica respuesta y estructura de datos retornados.
        """
        new_user = test_data['new_user']
        response = client.post(Endpoints.USERS, data=new_user)
        assert response.status_code == 201
        created_user = response.json()
        assert 'id' in created_user
        assert created_user['name'] == new_user['name']
        assert created_user['email'] == new_user['email']

    def test_get_user_by_id(self, client):
        """Prueba funcional: Obtener usuario específico.

        QA: Verifica recuperación individual de recursos.
        """
        user_id = 1
        response = client.get(Endpoints.get_user_by_id(user_id))
        assert response.status_code == 200
        user = response.json()
        assert user['id'] == user_id

    def test_update_user(self, client, test_data):
        """Prueba funcional: Actualizar usuario existente.

        QA: Valida modificaciones de recursos.
        """
        user_id = 1
        update_data = test_data['update_user']
        response = client.put(Endpoints.get_user_by_id(user_id), data=update_data)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user['name'] == update_data['name']

    def test_delete_user(self, client):
        """Prueba funcional: Eliminar usuario.

        QA: Verifica eliminación exitosa de recursos.
        """
        user_id = 2
        response = client.delete(Endpoints.get_user_by_id(user_id))
        assert response.status_code == 204

        # Verificar que ya no existe
        response = client.get(Endpoints.get_user_by_id(user_id), expected_status=404)