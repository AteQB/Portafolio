import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.soat_page import SoatPage
import time

@pytest.fixture(scope="function")
def driver():
    """Fixture para crear y configurar el driver de Selenium con Chrome."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    yield driver
    driver.quit()

def test_cotizar_soat_bng018(driver):
    """Cotiza SOAT para auto con placa BNG 018 (datos en duro)."""

    # Datos en duro
    placa = "BNG018"
    tipo_vehiculo = "auto"

    print("\n=== INICIANDO COTIZACIÓN SOAT DESDE HOME ===")

    soat = SoatPage(driver)

    # Paso 1: Navegar desde home hasta cotización SOAT
    print("PASO 1: Navegando desde home hasta cotización SOAT...")
    soat.navigate_to_home_and_cotizar()
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

    print("\n=== COTIZACION COMPLETADA EXITOSAMENTE ===")
    assert len(resultado) > 0

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

    print("\n=== COTIZACION COMPLETADA ===")
    assert len(resultado) > 0