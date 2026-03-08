# SOAT Cotizador - Automatización La Positiva

Automatización para cotizar **SOAT** (Seguro Obligatorio de Accidentes de Tránsito) en La Positiva usando **Selenium** con patrón **Page Object Model (POM)**.

---

## 📋 Estructura del Proyecto

```
1. Automatización Web Selenium Python/
├── pages/                      # Page Objects (Lógica de interacción con UI)
│   ├── base_page.py           # Clase base con métodos comunes
│   ├── home_page.py           # Página principal (DEPRECADO - usar SoatPage)
│   └── soat_page.py           # Página de cotización SOAT
│
├── tests/                      # Tests (Casos de prueba)
│   └── test_soat.py           # Test principal de cotización con datos Excel
│
├── utils/                      # Utilidades
│   ├── config.py              # Configuración del navegador
│   └── data_reader.py         # Lectura de datos desde Excel
│
├── data/                       # Datos de prueba
│   └── test_data.xlsx         # Excel con datos para parametrizar pruebas
│
├── screenshots_*/              # Capturas de pantalla por placa
├── requirements.txt            # Dependencias Python
└── README.md                   # Este archivo
```

---

## 🚀 Instalación y Ejecución

### **Paso 1: Instalar Dependencias**

```bash
pip install -r requirements.txt
```

Instala automáticamente:
- `selenium==4.x` - Automatización web
- `pytest==7.x` - Framework de testing  
- `openpyxl==3.x` - Lectura de Excel
- `webdriver-manager==4.x` - Gestión de ChromeDriver

### **Paso 2: Ejecutar el Test**

```bash
pytest tests/test_soat.py::test_cotizar_soat -v -s
```

**Parámetros:**
- `-v`: Verbose (muestra más detalles)
- `-s`: Show (muestra los prints del código)

### **Paso 3: Revisar Evidencias**

Las capturas de pantalla se guardan automáticamente en carpetas como:
- `screenshots_ABC_123/` - Screenshots para placa ABC-123
- `screenshots_XYZ_456/` - Screenshots para placa XYZ-456

Cada carpeta contiene:
1. `01_navegacion_cotizador.png` - Ingreso al cotizador
2. `02_seleccion_auto.png` - Selección del tipo de vehículo
3. `03_ingreso_placa.png` - Ingreso de placa
4. `04_aceptacion_politicas.png` - Checkboxes marcados y botón
5. `05_cotizacion_iniciada.png` - Después de presionar cotizar
6. `06_resultado_cotizacion.png` - Resultado final

---

## 📊 Datos de Prueba

El archivo `data/test_data.xlsx` contiene:
- **Columna A (placa)**: Número de placa (ej: ABC-123)
- **Columna B (tipo_vehiculo)**: Tipo de vehículo (auto, camioneta, moto)
- **Columna C (expected_result)**: Resultado esperado

El test ejecutará automáticamente todos los casos definidos en Excel.

---

## 🔧 Flujo de Cotización

1. ✅ **Navegación directa** al cotizador de SOAT
2. ✅ **Selección de tipo** de vehículo (auto/camioneta/moto)
3. ✅ **Ingreso de placa** desde datos Excel
4. ✅ **Aceptación de políticas**:
   - Finalidades Secundarias
   - Políticas de Privacidad
5. ✅ **Presión del botón** "Vamos por tu SOAT"
6. ✅ **Obtención de resultado** y validación

---

## 📝 Selectores Confirmados

```python
CAMPO_PLACA = (By.ID, "iplaca-home")
CHK_FINALIDADES = (By.ID, "flagFinalidadesSecundarias")
CHK_PRIVACIDAD = (By.ID, "flagPoliticaPrivacidad")
BTN_COTIZAR = (By.ID, "btngo")
CARD_AUTO = (By.CSS_SELECTOR, ".lq-slide__card-item:first-child")
CARD_MOTO = (By.CSS_SELECTOR, ".lq-slide__card-item:last-child")
```

---

## ⚙️ Configuración

Ver `utils/config.py` para ajustar:
- `BROWSER_HEADLESS` - Mostrar/ocultar navegador (default: False)

**Flags explicados:**
- `-v` → Verbose (muestra detalles de ejecución)
- `-s` → Show (muestra los prints dentro del código)

### **Paso 3: Ver la Ejecución en Tiempo Real**

El navegador Chromium se abrirá automáticamente y verás:
1. Página cargando el cotizador
2. Selección de tipo de vehículo (auto)
3. Ingreso de placa (BNG018)
4. Marcado de checkboxes
5. Click en botón cotizar
6. Resultado con precio

---

## 🔄 Flujo de Cotización Automatizado

El test ejecuta estos **6 pasos** en orden:

### **PASO 1️⃣: Navegación al Cotizador**
```
URL: https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador
Acción: Abrir página del cotizador
Resultado: Página cargada correctamente
```

### **PASO 2️⃣: Seleccionar Tipo de Vehículo**
```
Elemento: span.lq-slider-carddetail__info
Tipo: Hacer click en "Auto"
Acción: Selecciona categoría de vehículo (auto/moto)
Resultado: Tipo de vehículo seleccionado
```

### **PASO 3️⃣: Ingresar Número de Placa**
```
Elemento: #iplaca-home (input type="text")
Datos: BNG018
Acciones:
  1. Escribir número de placa
  2. Presionar TAB para validar
  3. Campo se autoformatea a BNG-018
Resultado: Placa validada
```

### **PASO 4️⃣: Aceptar Términos y Políticas**
```
Checkbox 1: #flagFinalidadesSecundarias
  → "Acepto uso de datos para finalidades secundarias"
Checkbox 2: #flagPoliticaPrivacidad
  → "Acepto las Políticas de Privacidad"
Acción: Marcar ambos checkboxes
Aplicación: JavaScript directo (más confiable)
Resultado: Ambos marcados (checked=True)
```

### **PASO 5️⃣: Presionar Botón Cotizar**
```
Elemento: #btngo (link con clase lq-btn)
Texto: "Vamos por tu SOAT"
Acción: Click en botón para iniciar cotización
Aplicación: JavaScript directo
Resultado: Cotización iniciada
```

### **PASO 6️⃣: Obtener Resultado**
```
Búsqueda: Contenido con "S/" (Soles peruanos)
Validación: Si encuentra "S/" = precio obtenido
Resultado: Cotización completada exitosamente
```

---

## 📁 Descripción Detallada de Archivos

### `pages/base_page.py`
Clase padre para todos los Page Objects. Contiene:
```python
class BasePage:
    def navigate_to(url)      # Navegar a URL
    def wait_for_element()    # Esperar elemento visible
```

### `pages/home_page.py`
Page Object para página inicial:
```python
class HomePage(BasePage):
    def go_to_cotizador()     # Ir directo al cotizador
```

### `pages/soat_page.py`
Page Object principal con toda la lógica de cotización:
```python
class SoatPage(BasePage):
    def select_tipo_vehiculo(tipo)    # Selecciona auto/moto
    def fill_placa(placa)             # Ingresa placa + TAB
    def accept_policies()             # Marca 2 checkboxes
    def cotizar()                     # Click en botón
    def get_resultado()               # Obtiene resultado
```

### `tests/test_soat.py`
Test principal que orquesta todo:
```python
def test_cotizar_soat_bng018():
    # 1. Navega y carga cotizador
    # 2. Selecciona auto
    # 3. Ingresa BNG018
    # 4. Acepta términos
    # 5. Presiona botón
    # 6. Verifica resultado
```

### `utils/config.py`
Configuración global:
```python
BROWSER_HEADLESS = False     # Ver navegador en pantalla
```

### `utils/data_reader.py`
Lee datos desde Excel (para futuros usos):
```python
class DataReader:
    @staticmethod
    def read_soat_data()  # Lee datos del Excel
```

### `data/test_data.xlsx`
Archivo Excel con columnas:
| placa   | tipo     |
|---------|----------|
| BNG018  | auto     |
| ABC123  | auto     |
| XYZ789  | moto     |

---

## 🔧 Selectores CSS Utilizados

| Elemento | Selector | Tipo HTML |
|----------|----------|-----------|
| Tipo vehículo | `span.lq-slider-carddetail__info` | `<span>` |
| Campo placa | `#iplaca-home` | `<input type="text">` |
| Finalidades | `#flagFinalidadesSecundarias` | `<input type="checkbox">` |
| Privacidad | `#flagPoliticaPrivacidad` | `<input type="checkbox">` |
| Botón cotizar | `#btngo` | `<a class="lq-btn">` |

---

## ⚙️ Tecnologías Utilizadas

| Herramienta | Versión | Propósito |
|-------------|---------|----------|
| Python | 3.14.3 | Lenguaje principal |
| Playwright | 1.58.0 | Automatización web |
| Pytest | 9.0.2 | Framework de testing |
| Openpyxl | 3.1.2 | Manejo de archivos Excel |

---

## 🎯 Patrón Implementado: Page Object Model (POM)

**Ventajas:**
- ✅ Separación de lógica UI en clases
- ✅ Reutilización de métodos
- ✅ Fácil mantenimiento
- ✅ Si cambia un selector, se actualiza en un solo lugar

**Ejemplo:**
```python
# En soat_page.py
def fill_placa(self, placa):
    elemento = self.page.locator('#iplaca-home')
    elemento.fill(placa)
    elemento.press('Tab')

# En test_soat.py
soat = SoatPage(page)
soat.fill_placa('BNG018')  # Reutilizable
```

---

## 💡 Nota sobre JavaScript en Playwright

En la función `accept_policies()` y `cotizar()` usamos JavaScript directo:

```python
self.page.evaluate("""
    () => {
        let elem = document.querySelector('#selector');
        if (elem) { elem.click(); }
    }
""")
```

**¿Por qué?** Algunos elementos están "outside of viewport" y Playwright no puede interactuar. JavaScript lo hace directamente en el navegador.

---

## 📊 Flujo de Ejecución Visual

```
┌─────────────────────────────────────────┐
│  pytest tests/test_soat.py -v -s       │
└────────────┬────────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ Abrir navegador    │
    │ Chromium headless  │
    │      false         │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ Navegar a cotizador        │
    │ https://lapositiva.com.pe/│
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ Seleccionar tipo vehículo  │
    │ (auto)                     │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ Ingresar placa BNG018      │
    │ + Presionar TAB            │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ Marcar 2 checkboxes        │
    │ JavaScript directo         │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ Presionar botón cotizar    │
    │ JavaScript directo         │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ Obtener resultado          │
    │ Buscar "S/" en página      │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ TEST PASSED                │
    │ ✅ Cotización exitosa      │
    └────────────────────────────┘
```

---

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| Selectores no funcionan | Inspecciona con DevTools (F12) y actualiza en el Page Object |
| Elemento no visible | Verifica que el scroll esté en el lugar correcto |
| Botón no responde | Usa JavaScript directo si está fuera de viewport |
| Test cuelga | Aumenta timeouts en `wait_for_load_state()` |

---

## 📝 Ejemplo de Salida Completa

```bash
$ pytest tests/test_soat.py::test_cotizar_soat_bng018 -v -s

=============== test session starts ===============
platform win32 -- Python 3.14.3
collected 1 item

tests/test_soat.py::test_cotizar_soat_bng018
=== INICIANDO COTIZACIÓN SOAT ===
PASO 1: Navegando al cotizador...
[OK] Página del cotizador cargada

PASO 2: Seleccionando tipo de vehículo: auto...
[OK] Tipo de vehículo seleccionado

PASO 3: Ingresando placa: BNG018...
[OK] Placa ingresada correctamente

PASO 4: Aceptando políticas de privacidad...
[OK] Finalidades Secundarias MARCADAS (checked=True)
[OK] Politicas de Privacidad MARCADAS (checked=True)

PASO 5: Presionando botón cotizar...
[OK] CLIC EN BOTON EJECUTADO - Cotizacion iniciada

PASO 6: Obteniendo resultado...
[OK] Cotizacion realizada exitosamente con precio en Soles

=== COTIZACIÓN COMPLETADA ===
PASSED [100%]

=============== 1 passed in 24.92s ===============
```

---

## 🎓 Próximas Mejoras (Opcionales)

- [ ] Parametrizar con múltiples placas desde Excel
- [ ] Validar montos de cotización
- [ ] Captura automática de screenshots en errores
- [ ] Reportes HTML interactivos
- [ ] Configurar GitHub Actions para CI/CD

---

## ✅ Resumen

Este proyecto automatiza completamente el flujo de cotización SOAT en La Positiva:

1. **Estructura limpia** con Page Object Model
2. **Código reutilizable** y fácil de mantener
3. **Ejecución transparente** con navegador visible
4. **Error handling** robusto con JavaScript
5. **Documentación clara** paso a paso

¡Listo para usar! Solo ejecuta `pytest tests/test_soat.py::test_cotizar_soat_bng018 -v -s` 🚀