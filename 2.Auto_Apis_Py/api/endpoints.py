"""
Definición de endpoints API.

Enfoque QA: Centralizar URLs de endpoints para facilitar mantenimiento.
Permite cambiar rutas sin modificar pruebas individuales.
"""

class Endpoints:
    # Endpoints de ejemplo para una API de usuarios
    USERS = '/users'
    USER_BY_ID = '/users/{user_id}'
    POSTS = '/posts'
    POST_BY_ID = '/posts/{post_id}'

    @staticmethod
    def get_user_by_id(user_id):
        """
        QA: Método para construir URLs dinámicas de forma segura.
        """
        return Endpoints.USER_BY_ID.format(user_id=user_id)

    @staticmethod
    def get_post_by_id(post_id):
        return Endpoints.POST_BY_ID.format(post_id=post_id)