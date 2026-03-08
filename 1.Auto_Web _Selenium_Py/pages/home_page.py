from .base_page import BasePage

class HomePage(BasePage):
    """Page Object para navegar a la sección de cotización SOAT.
    
    NOTA: Este archivo se mantiene por compatibilidad, pero actualmente 
    la navegación se realiza directamente desde SoatPage.navigate_to_cotizador()
    que accede al cotizador de forma directa sin pasar por el home.
    """

    def __init__(self, page):
        super().__init__(page)

    def go_to_cotizador(self):
        """Navega directamente al cotizador SOAT.
        
        DEPRECADO: Use SoatPage.navigate_to_cotizador() en su lugar.
        """
        self.navigate_to('https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador')