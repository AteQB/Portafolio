from .base_page import BasePage

class HomePage(BasePage):
    """Page Object para navegar a la sección de cotización SOAT."""

    def __init__(self, page):
        super().__init__(page)

    def go_to_cotizador(self):
        """Navega directamente al cotizador SOAT."""
        self.navigate_to('https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador')