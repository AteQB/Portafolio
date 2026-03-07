import os

class Config:
    """
    Clase de configuración para el proyecto.
    Objetivo: Centralizar todas las configuraciones (URLs, opciones de navegador, timeouts) para facilitar ajustes globales.
    """

    BASE_URL = "https://www.lapositiva.com.pe"  # URL base del sitio web objetivo
    BROWSER_HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"  # Ejecutar navegador en modo headless (sin UI) por defecto
    TIMEOUT = 30000  # Timeout en ms para esperas de elementos