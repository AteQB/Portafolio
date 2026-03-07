import pytest
from playwright.sync_api import Page
from pages.soat_page import SoatPage
import time

@pytest.fixture(scope="function")
def browser_context(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    yield context
    context.close()
    browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    return browser_context.new_page()

def test_cotizar_soat_bng018(page: Page):
    """Cotiza SOAT para auto con placa BNG 018 (datos en duro)."""
    
    # Datos en duro
    placa = "BNG018"
    tipo_vehiculo = "auto"
    
    print("\n=== INICIANDO COTIZACIÓN SOAT ===")
    
    soat = SoatPage(page)
    
    # Paso 1: Navegar al cotizador
    print("PASO 1: Navegando al cotizador...")
    soat.navigate_to('https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador')
    time.sleep(3)
    print("[OK] Página del cotizador cargada")
    
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
    
    print("\n=== COTIZACION COMPLETADA ===")
    assert len(resultado) > 0