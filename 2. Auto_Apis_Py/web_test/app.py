"""
Aplicación web de prueba para APIs.

Enfoque QA: Servidor simple con endpoints REST para probar el framework.
Permite ejecutar pruebas funcionales contra una API real simulada.
Ejecutar con: python web_test/app.py
"""

from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

# Datos simulados en memoria (para QA: simula base de datos)
users = [
    {"id": 1, "name": "Juan Pérez", "email": "juan@example.com"},
    {"id": 2, "name": "María García", "email": "maria@example.com"}
]

posts = [
    {"id": 1, "title": "Primer post", "content": "Contenido del primer post", "user_id": 1}
]

@app.route('/users', methods=['GET'])
def get_users():
    """Endpoint para obtener usuarios.

    QA: Retorna lista de usuarios en formato JSON.
    """
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    """Endpoint para crear usuario.

    QA: Valida datos de entrada y crea nuevo usuario.
    """
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        abort(400, "Datos inválidos: se requieren 'name' y 'email'")

    new_user = {
        "id": max([u['id'] for u in users] + [0]) + 1,
        "name": request.json['name'],
        "email": request.json['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint para obtener usuario específico.

    QA: Retorna usuario por ID o 404 si no existe.
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(404, "Usuario no encontrado")
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Endpoint para actualizar usuario.

    QA: Modifica usuario existente.
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(404, "Usuario no encontrado")

    if not request.json:
        abort(400, "Datos requeridos")

    user['name'] = request.json.get('name', user['name'])
    user['email'] = request.json.get('email', user['email'])
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Endpoint para eliminar usuario.

    QA: Remueve usuario de la lista.
    """
    global users
    users = [u for u in users if u['id'] != user_id]
    return '', 204

@app.route('/posts', methods=['GET'])
def get_posts():
    """Endpoint para obtener posts."""
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    """Endpoint para crear post."""
    if not request.json or 'title' not in request.json:
        abort(400, "Datos inválidos")

    new_post = {
        "id": max([p['id'] for p in posts] + [0]) + 1,
        "title": request.json['title'],
        "content": request.json.get('content', ''),
        "user_id": request.json.get('user_id', 1)
    }
    posts.append(new_post)
    return jsonify(new_post), 201

if __name__ == '__main__':
    print("Iniciando servidor de prueba en http://localhost:5000")
    print("QA: Ejecuta las pruebas con: pytest tests/test_api.py")
    app.run(debug=True, port=5000)