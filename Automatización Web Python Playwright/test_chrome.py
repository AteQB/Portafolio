from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.soat_page import SoatPage
import time

def test_chrome_setup():
    """Test para verificar que Chrome funciona correctamente."""
    print("Iniciando test de configuración de Chrome...")

    try:
        # Configurar Chrome
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print("✓ Driver de Chrome creado exitosamente")

        # Crear página
        soat = SoatPage(driver)

        # Probar navegación al home
        print("Navegando al home...")
        soat.navigate_to('https://www.lapositiva.com.pe/')
        time.sleep(3)

        print("✓ Navegación exitosa")

        # Probar navegación a cotización
        print("Navegando a cotización...")
        soat.navigate_to_home_and_cotizar()
        time.sleep(3)

        print("✓ Navegación a cotización exitosa")

        # Verificar elementos básicos
        try:
            placa_field = driver.find_element("id", "iplaca-home")
            print("✓ Campo de placa encontrado")
        except:
            print("✗ Campo de placa no encontrado")

        try:
            button = driver.find_element("id", "btngo")
            disabled = button.get_attribute("disabled")
            print(f"✓ Botón encontrado - Deshabilitado: {disabled}")
        except:
            print("✗ Botón no encontrado")

        driver.quit()
        print("✓ Test completado exitosamente!")

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    test_chrome_setup()