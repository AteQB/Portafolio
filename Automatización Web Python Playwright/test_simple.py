from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pages.soat_page import SoatPage
import time

def test_simple():
    """Test simple para verificar que Selenium funciona."""
    print("Iniciando test simple con Firefox...")

    try:
        # Configurar Firefox
        service = FirefoxService(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(service=service, options=options)

        print("Driver creado exitosamente")

        # Crear página
        soat = SoatPage(driver)

        # Navegar
        print("Navegando a la página...")
        soat.navigate_to('https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador')
        time.sleep(5)

        print("Página cargada. Cerrando...")
        driver.quit()
        print("Test completado exitosamente!")

    except Exception as e:
        print(f"Error: {str(e)}")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    test_simple()