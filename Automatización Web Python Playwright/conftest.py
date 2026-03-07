# conftest.py
"""
Configuración global para pytest en el proyecto de automatización.
Objetivo: Proporcionar fixtures y configuraciones compartidas para todas las pruebas, integrando Playwright con pytest.
"""

import pytest
from playwright.sync_api import Playwright

@pytest.fixture(scope="session")
def playwright():
    """
    Fixture para inicializar Playwright.
    Objetivo: Disponibilizar la instancia de Playwright para crear navegadores en las pruebas.
    """
    with pytest.importorskip("playwright"):
        import playwright.sync_api as pw
        return pw