from .base_page import BasePage

class SoatPage(BasePage):
    """
    Page Object para la página de cotización de SOAT.
    Objetivo: Manejar todas las interacciones del formulario de cotización, permitiendo reutilización en múltiples pruebas.
    """

    def __init__(self, page):
        """
        Inicializa la SoatPage.
        Objetivo: Preparar para interacciones con el formulario de SOAT.
        """
        super().__init__(page)

    def fill_placa(self, placa: str):
        """
        Llena el campo de placa del vehículo.
        Objetivo: Ingresar la placa como parte del proceso de cotización.
        Nota: Selector placeholder; ajusta a '#placa' o similar según el sitio.
        """
        self.fill_input("#placa", placa)  # Selector ejemplo

    def select_tipo_vehiculo(self, tipo: str):
        """
        Selecciona el tipo de vehículo desde un dropdown.
        Objetivo: Especificar el tipo de vehículo para la cotización.
        Nota: Selector placeholder; ajusta según el elemento real.
        """
        self.page.select_option("#tipo-vehiculo", tipo)

    def click_cotizar(self):
        """
        Hace clic en el botón de cotizar.
        Objetivo: Enviar el formulario y obtener la cotización.
        Nota: Selector placeholder; ajusta a '#btn-cotizar' o similar.
        """
        self.click_element("#btn-cotizar")

    def get_cotizacion_result(self) -> str:
        """
        Obtiene el texto del resultado de la cotización.
        Objetivo: Extraer el resultado para verificaciones en pruebas.
        Nota: Selector placeholder; ajusta según donde aparezca el resultado.
        """
        return self.get_text("#resultado-cotizacion")