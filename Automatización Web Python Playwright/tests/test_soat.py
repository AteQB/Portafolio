import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.soat_page import SoatPage
from utils.config import Config
from utils.data_reader import DataReader

# Cargar datos del Excel
data_reader = DataReader("data/test_data.xlsx")
soat_data = data_reader.read_soat_data()

@pytest.fixture(scope="function")
def browser_context(playwright):
    browser = playwright.chromium.launch(headless=Config.BROWSER_HEADLESS)
    context = browser.new_context()
    yield context
    context.close()
    browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page

@pytest.mark.parametrize("test_data", soat_data)
def test_cotizar_soat(page: Page, test_data):
    """
    Prueba para cotizar SOAT usando datos parametrizados del Excel.
    Objetivo: Verificar que la cotización funcione con diferentes datos de entrada.
    Acciones:
    - Navegar a la página principal.
    - Hacer clic en el enlace de SOAT.
    - Llenar el formulario con placa y tipo de vehículo.
    - Hacer clic en cotizar.
    - Verificar el resultado esperado.
    """
    home_page = HomePage(page)
    home_page.go_to_home()

    # Navegar a SOAT
    home_page.click_soat_link()

    soat_page = SoatPage(page)
    soat_page.fill_placa(test_data['placa'])
    soat_page.select_tipo_vehiculo(test_data['tipo_vehiculo'])
    soat_page.click_cotizar()

    result = soat_page.get_cotizacion_result()
    assert test_data['expected_result'].lower() in result.lower()