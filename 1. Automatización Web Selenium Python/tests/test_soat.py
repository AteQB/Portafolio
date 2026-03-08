import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.soat_page import SoatPage
from utils.data_reader import DataReader
import time
import os

@pytest.fixture(scope="function")
def driver():
    """Fixture para crear y configurar el driver de Selenium con Chrome."""
    # Usar ruta específica del chromedriver que funciona
    service = Service("C:\\Users\\quint\\.wdm\\drivers\\chromedriver\\win64\\145.0.7632.117\\chromedriver-win32\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def test_data():
    """Fixture para cargar datos de prueba desde Excel."""
    data_reader = DataReader("data/test_data.xlsx")
    return data_reader.read_soat_data()

def test_cotizar_soat(driver, test_data):
    """Cotiza SOAT usando datos del archivo Excel."""
    for test_case in test_data:
        placa = test_case["placa"]
        tipo_vehiculo = test_case["tipo_vehiculo"]
        expected = test_case["expected_result"]

        print(f"\n=== INICIANDO COTIZACIÓN SOAT PARA PLACA: {placa} ===")

        # Crear directorio para screenshots con nombre único
        screenshots_dir = f"screenshots_{placa.replace('-', '_')}"
        os.makedirs(screenshots_dir, exist_ok=True)

        soat = SoatPage(driver, screenshots_dir)

        # Paso 1: Navegar directo al cotizador
        print("PASO 1: Navegando al cotizador SOAT...")
        soat.navigate_to_cotizador()
        print("[OK] Navegación completada")

        # Paso 2: Seleccionar tipo de vehículo
        print(f"\nPASO 2: Seleccionando tipo de vehículo: {tipo_vehiculo}...")
        soat.select_tipo_vehiculo(tipo_vehiculo)
        print("[OK] Tipo de vehículo seleccionado")

        # Paso 3: Llenar placa
        print(f"\nPASO 3: Ingresando placa: {placa}...")
        soat.fill_placa(placa)
        print("[OK] Placa ingresada")

        # Paso 4: Aceptar políticas
        print("\nPASO 4: Aceptando políticas de privacidad...")
        soat.accept_policies()
        print("[OK] Políticas aceptadas")

        # Paso 5: Presionar botón cotizar
        print("\nPASO 5: Presionando botón cotizar...")
        soat.cotizar()
        print("[OK] Boton cotizar presionado")

        # Paso 6: Obtener resultado
        print("\nPASO 6: Obteniendo resultado...")
        resultado = soat.get_resultado()
        print(f"[OK] Resultado obtenido: {resultado}")

        print(f"\n=== COTIZACION COMPLETADA PARA {placa} ===")

        # Verificar que el resultado contenga algo esperado
        assert expected.lower() in resultado.lower() or "exitosa" in resultado.lower()