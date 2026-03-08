import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.soat_page import SoatPage
from utils.data_reader import DataReader
from utils.config import Config
import os

@pytest.fixture(scope="function")
def driver():
    """Fixture para crear y configurar el driver de Selenium con Chrome."""
    # Usar ruta específica del chromedriver que funciona
    service = Service("C:\\Users\\quint\\.wdm\\drivers\\chromedriver\\win64\\145.0.7632.117\\chromedriver-win32\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    
    if Config.BROWSER_MAXIMIZE:
        options.add_argument("--start-maximized")
    
    if Config.BROWSER_HEADLESS:
        options.add_argument("--headless")
    
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
    data_reader = DataReader(Config.DATA_FILE)
    return data_reader.read_soat_data()

def test_cotizar_soat(driver, test_data):
    """Cotiza SOAT usando datos del archivo Excel."""
    for test_case in test_data:
        placa = test_case["placa"]
        tipo_vehiculo = test_case["tipo_vehiculo"]
        expected = test_case["expected_result"]

        print(f"\n{'='*70}")
        print(f"INICIANDO COTIZACIÓN SOAT")
        print(f"Placa: {placa} | Vehículo: {tipo_vehiculo}")
        print(f"{'='*70}")

        # Crear directorio para screenshots con nombre único
        screenshots_dir = f"screenshots_{placa.replace('-', '_')}"
        os.makedirs(screenshots_dir, exist_ok=True)

        soat = SoatPage(driver, screenshots_dir)

        try:
            # Paso 1: Navegar directo al cotizador
            print("\n[1/6] Navegando al cotizador SOAT...")
            soat.navigate_to_cotizador()
            print("     ✓ Navegación completada")

            # Paso 2: Seleccionar tipo de vehículo
            print(f"\n[2/6] Seleccionando tipo de vehículo: {tipo_vehiculo}...")
            soat.select_tipo_vehiculo(tipo_vehiculo)
            print(f"     ✓ {tipo_vehiculo.upper()} seleccionado")

            # Paso 3: Llenar placa
            print(f"\n[3/6] Ingresando placa: {placa}...")
            soat.fill_placa(placa)
            print(f"     ✓ Placa ingresada")

            # Paso 4: Aceptar políticas
            print("\n[4/6] Aceptando políticas de privacidad...")
            soat.accept_policies()
            print("     ✓ Políticas aceptadas")

            # Paso 5: Presionar botón cotizar
            print("\n[5/6] Presionando botón cotizar...")
            soat.cotizar()
            print("     ✓ Botón presionado")

            # Paso 6: Obtener resultado
            print("\n[6/6] Obteniendo resultado...")
            resultado = soat.get_resultado()
            print(f"     ✓ Resultado: {resultado}")

            print(f"\n{'='*70}")
            print(f"VALIDACIÓN: {expected}")
            print(f"RESULTADO: {resultado}")
            print(f"{'='*70}")

            # Verificar que el resultado contenga algo esperado
            assert expected.lower() in resultado.lower() or "exitosa" in resultado.lower()
            
            print("\n✅ TEST PASÓ CORRECTAMENTE\n")

        except AssertionError as e:
            print(f"\n❌ TEST FALLÓ - Validación no cumplida\n")
            raise
        except Exception as e:
            print(f"\n❌ TEST CON ERROR: {str(e)}\n")
            raise