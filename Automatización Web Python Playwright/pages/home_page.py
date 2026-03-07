from .base_page import BasePage

class HomePage(BasePage):
    """
    Page Object para la página principal de La Positiva.
    Objetivo: Encapsular interacciones con la home page, como navegación inicial y acceso a secciones.
    """

    def __init__(self, page):
        """
        Inicializa la HomePage con la URL base.
        Objetivo: Preparar la página para interacciones.
        """
        super().__init__(page)
        self.url = "https://www.lapositiva.com.pe/wps/portal/corporativo/home"

    def go_to_home(self):
        """
        Navega a la página principal.
        Objetivo: Cargar la home page para iniciar el flujo de pruebas.
        """
        self.navigate_to(self.url)

    def click_soat_link(self):
        """
        Hace clic en el enlace de cotización de SOAT.
        Objetivo: Navegar desde la home a la sección de SOAT para proceder con la cotización.
        Nota: El selector es un placeholder; ajusta según el sitio real (ej. 'a[href*="soat"]').
        """
        self.click_element("a[href*='soat']")  # Selector ejemplo, cambiar según inspección