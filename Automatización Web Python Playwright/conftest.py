import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright():
    """Inicializa Playwright."""
    with sync_playwright() as p:
        yield p