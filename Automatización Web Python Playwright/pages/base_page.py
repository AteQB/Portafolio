from playwright.sync_api import Page

class BasePage:
    """
    Clase base para todos los Page Objects.
    Proporciona métodos comunes para interactuar con páginas web.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navega a una URL específica."""
        self.page.goto(url)

    def wait_for_element(self, selector: str):
        """Espera a que un elemento esté visible."""
        self.page.wait_for_selector(selector)