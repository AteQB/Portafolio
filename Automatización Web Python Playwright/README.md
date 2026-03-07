# Automatización Web Python Playwright

Este proyecto utiliza Playwright con Python para automatizar pruebas web, siguiendo el patrón Page Object Model (POM) para una estructura modular y reutilizable. El objetivo principal es crear pruebas automatizadas para cotizar SOAT en el sitio de La Positiva, permitiendo la reutilización de componentes y la parametrización de datos desde un archivo Excel.

## Estructura del Proyecto

- **pages/**: Contiene los Page Objects, que encapsulan la lógica de interacción con las páginas web para promover la reutilización y el mantenimiento.
  - `base_page.py`: Clase base que proporciona métodos comunes para todas las páginas, como navegación, clics, llenado de inputs y espera de elementos. Objetivo: Reducir código duplicado y centralizar operaciones básicas.
  - `home_page.py`: Page Object para la página principal de La Positiva. Incluye métodos para navegar a la home y hacer clic en el enlace de SOAT. Objetivo: Manejar la navegación inicial y acceso a secciones específicas.
  - `soat_page.py`: Page Object para la página de cotización de SOAT. Métodos para llenar la placa, seleccionar tipo de vehículo, hacer clic en cotizar y obtener resultados. Objetivo: Encapsular la lógica del formulario de cotización para facilitar pruebas y mantenimiento.

- **tests/**: Contiene los archivos de pruebas automatizadas.
  - `test_soat.py`: Prueba parametrizada para cotizar SOAT usando datos del Excel. Objetivo: Ejecutar múltiples escenarios de cotización con datos variables, verificando resultados esperados. Acciones: Navegar, interactuar con elementos, validar outputs.

- **utils/**: Utilidades y configuraciones para apoyar la automatización.
  - `config.py`: Archivo de configuración con URLs base, opciones de navegador y timeouts. Objetivo: Centralizar configuraciones para facilitar cambios globales.
  - `data_reader.py`: Clase para leer datos de prueba desde un archivo Excel. Objetivo: Proporcionar una interfaz reutilizable para cargar datos parametrizados, permitiendo que las pruebas usen datos externos sin hardcodear valores.

- **data/**: Carpeta para archivos de datos de prueba.
  - `test_data.xlsx`: Archivo Excel con datos de prueba para cotizaciones (placa, tipo_vehiculo, expected_result). Objetivo: Almacenar datos parametrizados para pruebas, facilitando la adición de nuevos escenarios sin modificar código.

- **requirements.txt**: Lista de dependencias Python necesarias (Playwright, pytest, openpyxl). Objetivo: Gestionar paquetes para reproducibilidad del entorno.

- **conftest.py**: Configuración de pytest para fixtures de Playwright. Objetivo: Configurar el entorno de pruebas de manera global.

- **create_excel.py**: Script para generar el archivo Excel de ejemplo. Objetivo: Crear datos de prueba iniciales; ejecutar una vez para generar `data/test_data.xlsx`.

## Instalación

1. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Instalar navegadores de Playwright:
   ```
   playwright install
   ```

3. Generar datos de prueba (opcional, si no existe el Excel):
   ```
   python create_excel.py
   ```

## Ejecutar Pruebas

Ejecutar todas las pruebas:
```
pytest
```

Ejecutar una prueba específica:
```
pytest tests/test_soat.py
```

Ejecutar con datos parametrizados (cada fila del Excel genera una prueba):
```
pytest tests/test_soat.py -v
```

## Ajustes Necesarios

- **Selectores**: Los selectores en `home_page.py` y `soat_page.py` son placeholders (ej. `#placa`). Inspecciona el sitio web de La Positiva para obtener los IDs/clases reales y actualízalos.
- **Datos de Prueba**: Edita `data/test_data.xlsx` para agregar más filas con placas, tipos de vehículo y resultados esperados.
- **Configuración**: Ajusta `utils/config.py` para headless mode, timeouts, etc., según necesidades.
- **Navegación**: Si el flujo de cotización requiere más pasos (ej. login), agrega métodos en los Page Objects.

Esta estructura permite escalar las pruebas agregando más Page Objects, tests y datos sin duplicar código.