from playwright.sync_api import Page

class BasePage:
    """
    Clase base para todos los Page Objects.
    Objetivo: Proporcionar métodos comunes reutilizables para interactuar con páginas web,
    reduciendo duplicación de código y facilitando el mantenimiento.
    """

    def __init__(self, page: Page):
        """
        Inicializa la página base con una instancia de Playwright Page.
        Objetivo: Establecer la conexión con la página para realizar acciones.
        """
        self.page = page

    def navigate_to(self, url: str):
        """
        Navega a una URL específica.
        Objetivo: Cargar la página web deseada en el navegador.
        """
        self.page.goto(url)

    def click_element(self, selector: str):
        """
        Hace clic en un elemento identificado por un selector CSS.
        Objetivo: Simular clics del usuario en botones, enlaces, etc.
        """
        self.page.click(selector)

    def fill_input(self, selector: str, text: str):
        """
        Llena un campo de input con texto.
        Objetivo: Ingresar datos en formularios de manera automatizada.
        """
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """
        Obtiene el texto de un elemento.
        Objetivo: Extraer contenido visible para verificaciones en pruebas.
        """
        return self.page.text_content(selector)

    def wait_for_element(self, selector: str):
        """
        Espera a que un elemento esté visible.
        Objetivo: Asegurar que la página haya cargado antes de interactuar.
        """
        self.page.wait_for_selector(selector)