from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    """
    Clase base para todos los Page Objects.
    Proporciona métodos comunes para interactuar con páginas web.
    """

    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url: str):
        """Navega a una URL específica."""
        self.driver.get(url)

    def wait_for_element(self, selector: str, by=By.CSS_SELECTOR):
        """Espera a que un elemento esté visible."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by, selector))
        )