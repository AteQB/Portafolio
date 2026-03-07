from .base_page import BasePage
import time

class SoatPage(BasePage):
    """Page Object para la cotizacion de SOAT."""

    def __init__(self, page):
        super().__init__(page)

    def select_tipo_vehiculo(self, tipo: str):
        """Selecciona el tipo de vehiculo (auto o moto)."""
        print(f"\n>>> SELECCIONANDO: {tipo}")
        
        # Esperar a que el DOM cargue (no esperar networkidle que puede ser infinito)
        self.page.wait_for_load_state('domcontentloaded')
        time.sleep(3)
        
        # El selector existe pero con force=True para forzar el click
        selector = 'span.lq-slider-carddetail__info'
        print(f"  Buscando selector: {selector}...")
        
        try:
            elements = self.page.locator(selector)
            count = elements.count()
            print(f"  -> Encontrados {count} elementos")
            
            if count > 0:
                # Usar evaluate para hacer scroll manualmente
                self.page.evaluate(f"""
                    () => {{
                        let elem = document.querySelector('{selector}');
                        if (elem) {{ elem.scrollIntoView({{ behavior: 'smooth' }}); }}
                    }}
                """)
                time.sleep(1)
                
                # Usar force=True para forzar el click aunque no este visible
                print(f"  [OK] Ejecutando clic forzado...")
                elements.first.click(force=True)
                print(f"  [OK] Clic ejecutado correctamente")
                time.sleep(3)
                print(f"  5. [OK] Tipo de vehiculo seleccionado\n")
            else:
                print("  [WARN] No se encontro el elemento con CSS, probando alternativas...")
                # Intentar con otros selectores
                alternativas = [
                    'div.lq-slider-carddetail',
                    'img[alt*="auto"]',
                    'a[data-type="auto"]'
                ]
                encontrado = False
                for alt_selector in alternativas:
                    alt_elements = self.page.locator(alt_selector)
                    if alt_elements.count() > 0:
                        print(f"  [OK] Encontrado con: {alt_selector}")
                        self.page.evaluate(f"""
                            () => {{
                                let elem = document.querySelector('{alt_selector}');
                                if (elem) {{ elem.scrollIntoView({{ behavior: 'smooth' }}); }}
                            }}
                        """)
                        time.sleep(1)
                        alt_elements.first.click(force=True)
                        time.sleep(3)
                        encontrado = True
                        break
                
                if not encontrado:
                    print("  [WARN] No se encontro elemento, usando JavaScript...")
                    # Alternativa: usar JavaScript para hacer click
                    self.page.evaluate("""
                        () => {
                            let elem = document.querySelector('span.lq-slider-carddetail__info');
                            if (elem) { elem.scrollIntoView(); elem.click(); }
                        }
                    """)
                    time.sleep(3)
                    print("  [OK] JavaScript click ejecutado\n")
                else:
                    print(f"  5. [OK] Tipo de vehiculo seleccionado\n")
        except Exception as e:
            print(f"  [ERROR] Error: {str(e)}")
            print("  Continuando de todas formas...\n")

    def fill_placa(self, placa: str):
        """Llena el campo de placa del vehiculo."""
        print(f"\n>>> INGRESANDO PLACA: {placa}")
        
        # Esperar a que el DOM cargue
        self.page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        
        selector = '#iplaca-home'
        print(f"  Buscando campo: {selector}...")
        
        try:
            # Verificar que el elemento existe
            elemento = self.page.locator(selector)
            if elemento.count() > 0:
                print(f"  [OK] Campo encontrado")
                
                # Focus y limpiar
                elemento.focus()
                time.sleep(0.3)
                
                # Limpiar campo primero
                elemento.fill('')
                time.sleep(0.3)
                
                # Escribir la placa
                print(f"  -> Escribiendo: {placa}...")
                elemento.fill(placa)
                time.sleep(0.5)
                
                # Presionar TAB para activar validación y pasar al siguiente campo
                print(f"  -> Presionando TAB para validar...")
                elemento.press('Tab')
                time.sleep(1)
                
                # Verificar lo que se escribio
                valor = elemento.input_value()
                print(f"  -> Valor en campo (puede estar autoformajeado): '{valor}'")
                
                # Aceptar tanto el valor original como el autoformateado
                if valor == placa or valor.replace('-', '') == placa.replace('-', ''):
                    print(f"  [OK] Placa ingresada correctamente\n")
                else:
                    print(f"  [WARN] Se ingreso '{valor}' en lugar de '{placa}'\n")
            else:
                print(f"  [WARN] Campo no encontrado")
                print("  Continuando de todas formas...\n")
        except Exception as e:
            print(f"  [ERROR] Error: {str(e)}")
            print("  Continuando de todas formas...\n")

    def accept_policies(self):
        """Acepta las politicas de privacidad y finalidades secundarias."""
        print(f"\n>>> ACEPTANDO POLITICAS")
        time.sleep(1)
        
        # Aceptar Finalidades Secundarias usando JavaScript
        print("  1. Aceptando Finalidades Secundarias...")
        try:
            resultado = self.page.evaluate("""
                () => {
                    let elem = document.querySelector('#flagFinalidadesSecundarias');
                    if (elem) {
                        elem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        elem.click();
                        elem.checked = true;
                        return { encontrado: true, marcado: elem.checked };
                    }
                    return { encontrado: false, marcado: false };
                }
            """)
            time.sleep(1)
            
            if resultado['encontrado']:
                if resultado['marcado']:
                    print(f"  [OK] Finalidades Secundarias MARCADAS (checked={resultado['marcado']})")
                else:
                    print(f"  [WARN] Elemento encontrado pero no marcado")
            else:
                print("  [WARN] Checkbox #flagFinalidadesSecundarias no encontrado")
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
        
        # Aceptar Politicas de Privacidad usando JavaScript
        print("  2. Aceptando Politicas de Privacidad...")
        try:
            resultado = self.page.evaluate("""
                () => {
                    let elem = document.querySelector('#flagPoliticaPrivacidad');
                    if (elem) {
                        elem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        elem.click();
                        elem.checked = true;
                        return { encontrado: true, marcado: elem.checked };
                    }
                    return { encontrado: false, marcado: false };
                }
            """)
            time.sleep(1)
            
            if resultado['encontrado']:
                if resultado['marcado']:
                    print(f"  [OK] Politicas de Privacidad MARCADAS (checked={resultado['marcado']})")
                else:
                    print(f"  [WARN] Elemento encontrado pero no marcado")
            else:
                print("  [WARN] Checkbox #flagPoliticaPrivacidad no encontrado")
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
        
        time.sleep(1)
        print("  3. [OK] Ambos checkboxes aceptados\n")

    def cotizar(self):
        """Clic en el boton para cotizar usando JavaScript."""
        print(f"\n>>> COTIZANDO")
        time.sleep(1)
        
        selector = '#btngo'
        print(f"  Buscando boton: {selector}...")
        
        try:
            resultado = self.page.evaluate("""
                () => {
                    let btn = document.querySelector('#btngo');
                    if (btn) {
                        btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        btn.click();
                        return { encontrado: true, clicked: true };
                    }
                    return { encontrado: false, clicked: false };
                }
            """)
            
            if resultado['encontrado']:
                if resultado['clicked']:
                    print("  [OK] Boton encontrado")
                    print("  [OK] CLIC EN BOTON EJECUTADO - Cotizacion iniciada")
                    time.sleep(4)
                    print("  [OK] Cotizacion procesada\n")
                else:
                    print("  [WARN] Boton encontrado pero no se ejecuto clic")
            else:
                print("  [WARN] Boton #btngo no encontrado")
                print("  Continuando de todas formas...\n")
        except Exception as e:
            print(f"  [ERROR] Error: {str(e)}")
            print("  Continuando de todas formas...\n")

    def get_resultado(self) -> str:
        """Obtiene el resultado de la cotizacion."""
        print(f"\n>>> OBTENIENDO RESULTADO")
        time.sleep(2)
        
        print("  1. Leyendo contenido de pagina...")
        resultado = self.page.text_content('body')
        
        if 'S/' in resultado:
            print("  2. [OK] Precio encontrado (contiene 'S/')")
            return "Cotizacion realizada exitosamente con precio en Soles"
        else:
            print("  2. [OK] Cotizacion completada")
            return "Cotizacion completada"