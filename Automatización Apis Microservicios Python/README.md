# Framework de Automatización de APIs - Enfoque QA

Este proyecto proporciona una estructura modular y reutilizable para automatizar pruebas funcionales de APIs REST en Python. Está diseñado con principios de Quality Assurance (QA) para asegurar confiabilidad, mantenibilidad y escalabilidad en las pruebas.

## Estructura del Proyecto

```
Automatización Apis Microservicios Python/
├── api/                    # Módulo de interacción con APIs
│   ├── __init__.py
│   ├── client.py          # Cliente HTTP reutilizable
│   └── endpoints.py       # Definición centralizada de endpoints
├── tests/                  # Casos de prueba funcionales
│   ├── __init__.py
│   └── test_api.py        # Pruebas con pytest
├── data/                   # Datos de prueba separados del código
│   └── test_data.json
├── utils/                  # Utilidades y configuraciones
│   ├── __init__.py
│   ├── config.py          # Configuraciones centralizadas
│   └── helpers.py         # Funciones auxiliares reutilizables
├── web_test/               # Servidor web de prueba
│   ├── __init__.py
│   └── app.py             # API REST simulada con Flask
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Esta documentación
```

## Principios QA Implementados

### 1. **Separación de Responsabilidades**
- **Código de prueba** separado de **datos de prueba**
- **Configuraciones** centralizadas para facilitar cambios de entorno
- **Utilidades** reutilizables para reducir duplicación

### 2. **Reutilización y Modularidad**
- Clase `APIClient` base para todas las interacciones HTTP
- Métodos comunes (GET, POST, PUT, DELETE) con validaciones estándar
- Fixtures de pytest para setup/teardown consistente

### 3. **Mantenibilidad**
- Endpoints definidos en un solo lugar
- Logging integrado para trazabilidad
- Configuración por variables de entorno

### 4. **Escalabilidad**
- Estructura preparada para múltiples APIs
- Fácil adición de nuevos casos de prueba
- Soporte para diferentes entornos (dev, staging, prod)

## Instalación y Configuración

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar entorno (opcional):**
   ```bash
   export API_BASE_URL=http://localhost:5000
   export LOG_LEVEL=DEBUG
   ```

## Uso

### 1. **Ejecutar Servidor de Prueba**
Para entender y probar la estructura, inicia el servidor web incluido:

```bash
python web_test/app.py
```

Esto inicia una API REST simulada en `http://localhost:5000` con endpoints para usuarios y posts.

### 2. **Ejecutar Pruebas**
```bash
pytest tests/test_api.py -v
```

Para reportes HTML:
```bash
pytest tests/test_api.py --html=reports/report.html
```

### 3. **Ejemplos de Uso en QA**

#### Prueba Funcional Básica
```python
from api.client import APIClient
from api.endpoints import Endpoints

client = APIClient()
response = client.get(Endpoints.USERS)
assert response.status_code == 200
```

#### Ingreso de Datos
```python
new_user = {"name": "Ana López", "email": "ana@example.com"}
response = client.post(Endpoints.USERS, data=new_user)
assert response.status_code == 201
```

## Casos de Prueba QA Incluidos

- ✅ **Obtener recursos** (GET)
- ✅ **Crear recursos** (POST)
- ✅ **Actualizar recursos** (PUT)
- ✅ **Eliminar recursos** (DELETE)
- ✅ **Validaciones de respuesta**
- ✅ **Manejo de errores** (404, 400)
- ✅ **Datos de prueba externos**

## Mejores Prácticas QA

1. **Usa fixtures** para setup consistente
2. **Separa datos de prueba** en archivos JSON
3. **Valida respuestas** en cada petición
4. **Loggea acciones** para debugging
5. **Configura timeouts** apropiados
6. **Prueba casos de error** además de casos felices

## Extensión del Framework

Para agregar nuevas APIs:

1. Define nuevos endpoints en `api/endpoints.py`
2. Crea métodos específicos en `APIClient` si es necesario
3. Agrega casos de prueba en `tests/`
4. Actualiza datos de prueba en `data/`

Esta estructura asegura que tus pruebas de API sean robustas, mantenibles y enfocadas en la calidad del software.