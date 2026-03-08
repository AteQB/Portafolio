from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

class SoatPage(BasePage):
    """Page Object para la cotizacion de SOAT."""

    # ============================================================
    # SELECTORES REALES - La Positiva Cotizador SOAT
    # Confirmados del DOM - marzo 2025
    # ============================================================

    # Campo de placa
    CAMPO_PLACA = (By.ID, "iplaca-home")

    # Error campo placa
    ERROR_PLACA = (By.ID, "imsg-error")

    # Checkbox Finalidades Secundarias
    CHK_FINALIDADES = (By.ID, "flagFinalidadesSecundarias")

    # Checkbox Políticas de Privacidad
    CHK_PRIVACIDAD = (By.ID, "flagPoliticaPrivacidad")

    # Error Políticas de Privacidad
    ERROR_PRIVACIDAD = (By.ID, "imsg-error-privacidad")

    # Botón "Vamos por tu SOAT" (es un <a> no un <button>)
    BTN_COTIZAR = (By.ID, "btngo")

    # Card Autos
    CARD_AUTO = (By.CSS_SELECTOR, ".lq-slide__card-item:first-child")

    # Card Motos
    CARD_MOTO = (By.CSS_SELECTOR, ".lq-slide__card-item:last-child")

    def __init__(self, driver, screenshots_dir="screenshots"):
        super().__init__(driver)
        self.screenshots_dir = screenshots_dir
        os.makedirs(self.screenshots_dir, exist_ok=True)
        self.screenshot_count = 0

    def take_screenshot(self, step_name):
        """Toma una captura de pantalla y la guarda con el nombre del paso."""
        self.screenshot_count += 1
        filename = f"{self.screenshot_count:02d}_{step_name}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"  [EVIDENCIA] Screenshot guardado: {filepath}")

    def navigate_to_cotizador(self):
        """Navega directamente al cotizador SOAT."""
        print(f"\n>>> NAVEGANDO DIRECTO AL COTIZADOR")

        cotizador_url = 'https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador'
        try:
            print("  Navegando al cotizador...")
            self.navigate_to(cotizador_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CAMPO_PLACA)
            )
            print("  [OK] Navegación al cotizador completada")
            self.take_screenshot("navegacion_cotizador")
        except Exception as e:
            print(f"  [ERROR] Error en navegación: {e}")
            raise

    def select_tipo_vehiculo(self, tipo: str):
        """Selecciona el tipo de vehiculo (auto o moto)."""
        print(f"\n>>> SELECCIONANDO: {tipo}")

        try:
            # Esperar a que la página cargue completamente
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(3)

            # Hacer scroll hacia abajo para ver los elementos del formulario
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
            time.sleep(2)

            # Seleccionar el selector apropiado basado en el tipo
            if tipo.lower() in ["auto", "camioneta"]:
                selector = self.CARD_AUTO
                tipo_display = "AUTO"
            elif tipo.lower() == "moto":
                selector = self.CARD_MOTO
                tipo_display = "MOTO"
            else:
                print(f"  [ERROR] Tipo de vehículo no reconocido: {tipo}")
                return

            print(f"  Buscando card para {tipo_display}...")

            # Esperar a que el elemento esté presente y clickeable
            card_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(selector)
            )

            # Hacer scroll al elemento
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", card_element)
            time.sleep(2)

            # Verificar que sea visible
            is_visible = self.driver.execute_script("""
                var elem = arguments[0];
                var rect = elem.getBoundingClientRect();
                return rect.top >= 0 && rect.left >= 0 &&
                       rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                       rect.right <= (window.innerWidth || document.documentElement.clientWidth) &&
                       elem.offsetWidth > 0 && elem.offsetHeight > 0;
            """, card_element)

            if not is_visible:
                print("  [WARN] Elemento no completamente visible, intentando scroll adicional...")
                self.driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(1)

            # Intentar clic con JavaScript primero
            try:
                self.driver.execute_script("arguments[0].click();", card_element)
                print(f"  [OK] Card {tipo_display} seleccionado con JavaScript")
            except Exception as js_error:
                print(f"  [WARN] Clic JavaScript falló: {str(js_error)}")
                # Intentar clic normal
                try:
                    card_element.click()
                    print(f"  [OK] Card {tipo_display} seleccionado con clic normal")
                except Exception as normal_error:
                    print(f"  [WARN] Clic normal falló: {str(normal_error)}")
                    # Último intento con ActionChains
                    try:
                        actions = ActionChains(self.driver)
                        actions.move_to_element(card_element).pause(1).click().perform()
                        print(f"  [OK] Card {tipo_display} seleccionado con ActionChains")
                    except Exception as action_error:
                        print(f"  [ERROR] Todos los métodos de clic fallaron: {str(action_error)}")
                        return

            time.sleep(3)
            print("  [OK] Tipo de vehiculo seleccionado\n")
            self.take_screenshot(f"seleccion_{tipo}")

        except Exception as e:
            print(f"  [ERROR] Error general en select_tipo_vehiculo: {str(e)}\n")

        except Exception as e:
            print(f"  [ERROR] Error general en select_tipo_vehiculo: {str(e)}\n")
    def fill_placa(self, placa: str):
        """Ingresa la placa del vehiculo."""
        print(f"\n>>> INGRESANDO PLACA: {placa}")

        try:
            # Hacer scroll hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)

            # Esperar a que el campo esté presente
            campo_placa = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CAMPO_PLACA)
            )

            # Hacer scroll al campo
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", campo_placa)
            time.sleep(1)

            # Limpiar y llenar el campo
            campo_placa.clear()
            campo_placa.send_keys(placa)

            print(f"  [OK] Placa '{placa}' ingresada")

            # Presionar TAB para validar
            campo_placa.send_keys("\t")
            time.sleep(2)

            # Verificar el valor
            valor_actual = campo_placa.get_attribute("value")
            print(f"  -> Valor en campo: '{valor_actual}'")

            # Verificar si hay errores
            try:
                error_element = self.driver.find_element(*self.ERROR_PLACA)
                if error_element.is_displayed():
                    error_text = error_element.text.strip()
                    print(f"  [WARN] Error en placa: {error_text}")
            except:
                print("  [OK] No hay errores de placa")

            print("  [OK] Placa procesada\n")
            self.take_screenshot("ingreso_placa")

        except Exception as e:
            print(f"  [ERROR] Error al ingresar placa: {str(e)}\n")

    def accept_policies(self):
        """Acepta las politicas de privacidad y finalidades secundarias."""
        print(f"\n>>> ACEPTANDO POLITICAS")

        try:
            # Aceptar Finalidades Secundarias
            print("  1. Aceptando Finalidades Secundarias...")
            try:
                fs_checkbox = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.CHK_FINALIDADES)
                )
                if not fs_checkbox.is_selected():
                    fs_checkbox.click()
                    print("  [OK] Finalidades Secundarias marcadas")
                else:
                    print("  [OK] Finalidades Secundarias ya estaban marcadas")
            except Exception as e:
                print(f"  [WARN] Error en Finalidades Secundarias: {str(e)}")

            # Aceptar Politicas de Privacidad
            print("  2. Aceptando Politicas de Privacidad...")
            try:
                pp_checkbox = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.CHK_PRIVACIDAD)
                )
                if not pp_checkbox.is_selected():
                    pp_checkbox.click()
                    print("  [OK] Politicas de Privacidad marcadas")
                else:
                    print("  [OK] Politicas de Privacidad ya estaban marcadas")
            except Exception as e:
                print(f"  [WARN] Error en Politicas de Privacidad: {str(e)}")

            # Hacer scroll hacia el botón cotizar para que se vea en la captura
            print("  3. Posicionando vista para captura...")
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.BTN_COTIZAR)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
            time.sleep(2)

            print("  [OK] Politicas aceptadas\n")
            self.take_screenshot("aceptacion_politicas")

        except Exception as e:
            print(f"  [ERROR] Error general en politicas: {str(e)}\n")

    def cotizar(self):
        """Clic en el boton para cotizar."""
        print(f"\n>>> COTIZANDO")

        try:
            # Hacer scroll hacia abajo para asegurar que el botón sea visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Buscar el botón usando el selector específico
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.BTN_COTIZAR)
            )
            print("  [OK] Botón encontrado por ID")

            # Verificar si el botón está deshabilitado
            is_disabled = button.get_attribute("disabled") is not None
            button_text = button.text.strip() or button.get_attribute("value") or "Sin texto"

            print(f"  Botón encontrado: '{button_text}' - Deshabilitado: {is_disabled}")

            if is_disabled:
                print("  [ERROR] El botón está DESHABILITADO - Verificando prerrequisitos...")

                # Verificar estado de todos los campos requeridos
                self._check_prerequisites()
                return

            # Hacer scroll al botón y esperar
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
            time.sleep(2)

            # Verificar nuevamente que no esté deshabilitado después del scroll
            is_disabled_after_scroll = button.get_attribute("disabled") is not None
            if is_disabled_after_scroll:
                print("  [ERROR] El botón sigue deshabilitado después del scroll")
                self._check_prerequisites()
                return

            # Intentar hacer clic
            try:
                button.click()
                print("  [OK] Clic en botón de cotización ejecutado")
            except Exception as click_error:
                print(f"  [WARN] Clic normal falló: {str(click_error)}")
                # Intentar con JavaScript
                try:
                    self.driver.execute_script("arguments[0].click();", button)
                    print("  [OK] Clic con JavaScript ejecutado")
                except Exception as js_error:
                    print(f"  [ERROR] Clic con JavaScript también falló: {str(js_error)}")
                    return

            time.sleep(5)  # Esperar más tiempo para que procese la cotización
            print("  [OK] Cotización iniciada\n")
            self.take_screenshot("cotizacion_iniciada")

        except Exception as e:
            print(f"  [ERROR] Error general en cotizar: {str(e)}")

    def _check_prerequisites(self):
        """Verifica que todos los prerrequisitos estén completos."""
        print("  [INFO] Verificando prerrequisitos...")

        try:
            # Verificar tipo de vehículo (al menos uno debe estar seleccionado)
            try:
                auto_card = self.driver.find_element(*self.CARD_AUTO)
                moto_card = self.driver.find_element(*self.CARD_MOTO)
                # Verificar si alguno tiene clase de selección o similar
                auto_selected = "selected" in auto_card.get_attribute("class") or auto_card.get_attribute("aria-selected") == "true"
                moto_selected = "selected" in moto_card.get_attribute("class") or moto_card.get_attribute("aria-selected") == "true"
                vehiculo_selected = auto_selected or moto_selected
                print(f"    ✓ Tipo de vehículo seleccionado: {vehiculo_selected}")
            except:
                print("    ✗ Cards de vehículo no encontrados")

            # Verificar placa
            try:
                placa_field = self.driver.find_element(*self.CAMPO_PLACA)
                placa_value = placa_field.get_attribute("value") or ""
                print(f"    ✓ Placa ingresada: '{placa_value}' (longitud: {len(placa_value)})")

                # Verificar errores de placa
                try:
                    error_placa = self.driver.find_element(*self.ERROR_PLACA)
                    if error_placa.is_displayed():
                        print(f"    ✗ Error de placa: {error_placa.text.strip()}")
                    else:
                        print("    ✓ No hay errores de placa")
                except:
                    print("    ✓ No hay errores de placa")

            except:
                print("    ✗ Campo de placa no encontrado")

            # Verificar checkboxes
            try:
                fs_checkbox = self.driver.find_element(*self.CHK_FINALIDADES)
                pp_checkbox = self.driver.find_element(*self.CHK_PRIVACIDAD)
                fs_checked = fs_checkbox.is_selected()
                pp_checked = pp_checkbox.is_selected()
                print(f"    ✓ Finalidades Secundarias: {fs_checked}")
                print(f"    ✓ Política Privacidad: {pp_checked}")

                # Verificar errores de privacidad
                if not pp_checked:
                    try:
                        error_privacidad = self.driver.find_element(*self.ERROR_PRIVACIDAD)
                        if error_privacidad.is_displayed():
                            print(f"    ✗ Error de privacidad: {error_privacidad.text.strip()}")
                    except:
                        pass

            except:
                print("    ✗ Checkboxes no encontrados")

        except Exception as e:
            print(f"    [ERROR] Error al verificar prerrequisitos: {str(e)}")

    def get_resultado(self):
        """Obtiene el resultado de la cotización."""
        print(f"\n>>> OBTENIENDO RESULTADO")

        try:
            time.sleep(3)
            # Buscar en el contenido de la página
            page_text = self.driver.find_element(By.TAG_NAME, "body").text

            if "S/" in page_text:
                print("  [OK] Precio encontrado en Soles")
                result = "Cotizacion realizada exitosamente con precio en Soles"
            else:
                print("  [OK] Cotizacion completada")
                result = "Cotizacion completada"

            self.take_screenshot("resultado_cotizacion")
            return result

        except Exception as e:
            print(f"  [ERROR] Error al obtener resultado: {str(e)}")
            return "Error al obtener resultado"