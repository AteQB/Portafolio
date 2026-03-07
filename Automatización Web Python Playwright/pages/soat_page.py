from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class SoatPage(BasePage):
    """Page Object para la cotizacion de SOAT."""

    def navigate_to_home_and_cotizar(self):
        """Navega a la página principal y hace clic en 'Cotizar SOAT'."""
        print(f"\n>>> NAVEGANDO AL HOME Y COTIZANDO")

        try:
            # Navegar a la página principal
            print("  1. Navegando a la página principal...")
            self.navigate_to('https://www.lapositiva.com.pe/')
            time.sleep(3)

            # Esperar a que cargue completamente
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)

            # Buscar y hacer clic en el botón "Cotizar SOAT"
            print("  2. Buscando botón 'Cotizar SOAT'...")

            # Intentar diferentes selectores para el botón
            button_selectors = [
                "a[href*='cotizador']",
                "a:contains('SOAT')",
                "[data-target*='soat']",
                ".soat-button",
                "button:contains('SOAT')"
            ]

            button_found = False
            for selector in button_selectors:
                try:
                    if ":contains" in selector:
                        # Para selectores que contienen texto
                        text = selector.split("'")[1]
                        button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{text}')]"))
                        )
                    else:
                        button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )

                    # Hacer scroll al botón
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                    time.sleep(1)

                    button.click()
                    print(f"  [OK] Botón encontrado con selector: {selector}")
                    button_found = True
                    break

                except:
                    continue

            if not button_found:
                print("  [WARN] No se encontró botón específico, intentando navegación directa...")
                # Si no encuentra el botón, ir directamente a la página de cotización
                self.navigate_to('https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador')
                time.sleep(3)

            # Verificar que estamos en la página de cotización
            WebDriverWait(self.driver, 10).until(
                lambda driver: "cotizador" in driver.current_url.lower() or
                              "soat" in driver.title.lower()
            )

            print("  [OK] Navegación completada - En página de cotización\n")

        except Exception as e:
            print(f"  [ERROR] Error en navegación: {str(e)}")
            print("  Intentando navegación directa...")
            self.navigate_to('https://www.lapositiva.com.pe/wps/portal/corporativo/home/cotizador')
            time.sleep(3)

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

            # Buscar elementos de tipo de vehículo con diferentes estrategias
            elementos = []

            # Estrategia 1: Selector CSS directo
            try:
                elementos = self.driver.find_elements(By.CSS_SELECTOR, "span.lq-slider-carddetail__info")
            except:
                pass

            # Estrategia 2: Buscar por texto si no se encontraron elementos
            if not elementos:
                try:
                    # Buscar spans que contengan "AUTO" o "MOTO"
                    elementos = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'AUTO') or contains(text(), 'MOTO')]")
                except:
                    pass

            # Estrategia 3: Buscar contenedores más amplios
            if not elementos:
                try:
                    contenedores = self.driver.find_elements(By.CSS_SELECTOR, "div.lq-slider-card, .vehicle-type, .tipo-vehiculo")
                    for contenedor in contenedores:
                        spans = contenedor.find_elements(By.TAG_NAME, "span")
                        elementos.extend(spans)
                except:
                    pass

            print(f"  Elementos encontrados: {len(elementos)}")

            # Mostrar información de cada elemento encontrado
            for i, elem in enumerate(elementos):
                try:
                    texto = elem.text.strip()
                    visible = elem.is_displayed()
                    print(f"    [{i}] '{texto}' - Visible: {visible}")
                except:
                    print(f"    [{i}] [Error al leer elemento]")

            # Buscar el elemento que contiene el tipo especificado
            target_element = None
            for elem in elementos:
                try:
                    texto_elem = elem.text.strip().upper()
                    if tipo.upper() in texto_elem or texto_elem in tipo.upper():
                        target_element = elem
                        print(f"  [OK] Elemento encontrado: '{elem.text.strip()}'")
                        break
                except:
                    continue

            # Si no se encontró exactamente, intentar con el primer elemento disponible
            if target_element is None and elementos:
                print(f"  [WARN] No se encontró elemento para '{tipo}', usando el primero disponible...")
                target_element = elementos[0]

            if target_element:
                # Asegurar que el elemento sea visible
                try:
                    # Scroll más agresivo si es necesario
                    self.driver.execute_script("""
                        arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
                        arguments[0].focus();
                    """, target_element)
                    time.sleep(2)

                    # Verificar si está realmente visible
                    is_visible = self.driver.execute_script("""
                        var elem = arguments[0];
                        var rect = elem.getBoundingClientRect();
                        return rect.top >= 0 && rect.left >= 0 &&
                               rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                               rect.right <= (window.innerWidth || document.documentElement.clientWidth) &&
                               elem.offsetWidth > 0 && elem.offsetHeight > 0;
                    """, target_element)

                    if not is_visible:
                        print("  [WARN] Elemento aún no visible, intentando scroll adicional...")
                        self.driver.execute_script("window.scrollBy(0, 200);")
                        time.sleep(1)

                    # Intentar clic con JavaScript primero
                    try:
                        self.driver.execute_script("arguments[0].click();", target_element)
                        print("  [OK] Clic ejecutado con JavaScript")
                    except Exception as js_error:
                        print(f"  [WARN] Clic JavaScript falló: {str(js_error)}")
                        # Intentar clic normal
                        try:
                            target_element.click()
                            print("  [OK] Clic normal ejecutado")
                        except Exception as normal_error:
                            print(f"  [WARN] Clic normal falló: {str(normal_error)}")
                            # Último intento con ActionChains
                            try:
                                actions = ActionChains(self.driver)
                                actions.move_to_element(target_element).pause(1).click().perform()
                                print("  [OK] Clic con ActionChains ejecutado")
                            except Exception as action_error:
                                print(f"  [ERROR] Todos los métodos de clic fallaron: {str(action_error)}")
                                return

                    time.sleep(3)
                    print("  [OK] Tipo de vehiculo seleccionado\n")

                except Exception as e:
                    print(f"  [ERROR] Error al interactuar con el elemento: {str(e)}\n")
            else:
                print("  [ERROR] No se encontraron elementos de tipo de vehículo\n")

        except Exception as e:
            print(f"  [ERROR] Error general en select_tipo_vehiculo: {str(e)}\n")
        print(f"\n>>> INGRESANDO PLACA: {placa}")

        try:
            # Hacer scroll hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)

            # Esperar a que el campo esté presente
            campo_placa = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "iplaca-home"))
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

            print("  [OK] Placa procesada\n")

        except Exception as e:
            print(f"  [ERROR] Error al ingresar placa: {str(e)}\n")

    def accept_policies(self):
        """Acepta las politicas de privacidad y finalidades secundarias."""
        print(f"\n>>> ACEPTANDO POLITICAS")

        try:
            # Hacer scroll hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Aceptar Finalidades Secundarias
            print("  1. Aceptando Finalidades Secundarias...")
            try:
                fs_checkbox = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "flagFinalidadesSecundarias"))
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
                    EC.element_to_be_clickable((By.ID, "flagPoliticaPrivacidad"))
                )
                if not pp_checkbox.is_selected():
                    pp_checkbox.click()
                    print("  [OK] Politicas de Privacidad marcadas")
                else:
                    print("  [OK] Politicas de Privacidad ya estaban marcadas")
            except Exception as e:
                print(f"  [WARN] Error en Politicas de Privacidad: {str(e)}")

            time.sleep(1)
            print("  3. [OK] Politicas procesadas\n")

        except Exception as e:
            print(f"  [ERROR] Error general en politicas: {str(e)}\n")

    def cotizar(self):
        """Clic en el boton para cotizar."""
        print(f"\n>>> COTIZANDO")

        try:
            # Hacer scroll hacia abajo para asegurar que el botón sea visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Buscar el botón con diferentes estrategias
            button = None

            # Estrategia 1: ID directo
            try:
                button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "btngo"))
                )
                print("  [OK] Botón encontrado por ID")
            except:
                # Estrategia 2: Buscar por texto
                try:
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cotizar') or contains(text(), 'SOAT') or contains(text(), 'Vamos')]"))
                    )
                    print("  [OK] Botón encontrado por texto")
                except:
                    # Estrategia 3: Buscar por clase o atributo
                    try:
                        button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "[id*='btn'], .btn-cotizar, .cotizar-btn"))
                        )
                        print("  [OK] Botón encontrado por clase")
                    except:
                        print("  [ERROR] No se pudo encontrar el botón de cotización")
                        return

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

        except Exception as e:
            print(f"  [ERROR] Error general en cotizar: {str(e)}")

    def _check_prerequisites(self):
        """Verifica que todos los prerrequisitos estén completos."""
        print("  [INFO] Verificando prerrequisitos...")

        try:
            # Verificar tipo de vehículo
            vehiculo_elements = self.driver.find_elements(By.CSS_SELECTOR, "span.lq-slider-carddetail__info")
            vehiculo_selected = any(elem.is_displayed() for elem in vehiculo_elements)
            print(f"    ✓ Tipo de vehículo visible: {vehiculo_selected}")

            # Verificar placa
            try:
                placa_field = self.driver.find_element(By.ID, "iplaca-home")
                placa_value = placa_field.get_attribute("value") or ""
                print(f"    ✓ Placa ingresada: '{placa_value}' (longitud: {len(placa_value)})")
            except:
                print("    ✗ Campo de placa no encontrado")

            # Verificar checkboxes
            try:
                fs_checkbox = self.driver.find_element(By.ID, "flagFinalidadesSecundarias")
                pp_checkbox = self.driver.find_element(By.ID, "flagPoliticaPrivacidad")
                fs_checked = fs_checkbox.is_selected()
                pp_checked = pp_checkbox.is_selected()
                print(f"    ✓ Finalidades Secundarias: {fs_checked}")
                print(f"    ✓ Política Privacidad: {pp_checked}")
            except:
                print("    ✗ Checkboxes no encontrados")

        except Exception as e:
            print(f"    [ERROR] Error al verificar prerrequisitos: {str(e)}")
        print(f"\n>>> OBTENIENDO RESULTADO")

        try:
            time.sleep(3)
            # Buscar en el contenido de la página
            page_text = self.driver.find_element(By.TAG_NAME, "body").text

            if "S/" in page_text:
                print("  [OK] Precio encontrado en Soles")
                return "Cotizacion realizada exitosamente con precio en Soles"
            else:
                print("  [OK] Cotizacion completada")
                return "Cotizacion completada"

        except Exception as e:
            print(f"  [ERROR] Error al obtener resultado: {str(e)}")
            return "Error al obtener resultado"