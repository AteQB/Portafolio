class Config:
    """Configuración del proyecto de Automatización SOAT."""
    
    # === NAVEGADOR ===
    BROWSER_HEADLESS = False  # False = mostrar navegador, True = ocultar
    BROWSER_MAXIMIZE = True   # Maximizar ventana del navegador
    
    # === URLs ===
    COTIZADOR_URL = 'https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador'
    HOME_URL = 'https://www.lapositiva.com.pe/'
    
    # === TIMEOUTS ===
    WAIT_TIMEOUT = 10  # Timeout default para WebDriverWait en segundos
    CLICK_WAIT = 5     # Timeout para clicks en elementos
    PAGE_LOAD_TIMEOUT = 15  # Timeout para carga de página
    
    # === DATOS ===
    DATA_FILE = "data/test_data.xlsx"  # Ruta del archivo de datos
    
    # === CAPTURAS ===
    SCREENSHOTS_DIR = "screenshots"  # Directorio base para screenshots
    TAKE_SCREENSHOTS = True  # Habilitar/deshabilitar capturas
    
    # === LOGS ===
    LOG_FILE = "test_execution.log"  # Archivo de log
    VERBOSE_MODE = True  # Mostrar logs detallados