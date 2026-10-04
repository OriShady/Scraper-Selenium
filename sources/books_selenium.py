import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Importar las configuraciones
from core.base_source import BaseScraper
from config import settings

class SeleniumScraper(BaseScraper):
    
    def __init__(self, url=settings.BASE_URL):
        # Inicializa la clase padre (url, datos, errores)
        super().__init__(url)
        self.driver = None
        self.wait = None

    def configurar_cliente(self):
        """Inicializa el navegador de Chrome."""
        print("Iniciando Selenium WebDriver...")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, settings.SELENIUM_TIMEOUT)

    def _extraer_libros(self):
        """Método interno equivalente a extraer_libros() original."""
        productos = self.driver.find_elements(By.CSS_SELECTOR, settings.SELECTORS["producto"])
        libros_pagina = []
        
        print(f"   Productos encontrados: {len(productos)}")
        
        for numero, producto in enumerate(productos, start=1):
            try:
                nombre = producto.find_element(By.CSS_SELECTOR, settings.SELECTORS["titulo"]).get_attribute("title")
                precio = producto.find_element(By.CSS_SELECTOR, settings.SELECTORS["precio"]).text
                url = producto.find_element(By.CSS_SELECTOR, settings.SELECTORS["titulo"]).get_attribute("href")
                rating = producto.find_element(By.CSS_SELECTOR, settings.SELECTORS["rating"]).get_attribute("class").split()[-1]
                
                libros_pagina.append({
                    "nombre": nombre,
                    "precio": precio,
                    "rating": rating,
                    "url": url
                })
            except NoSuchElementException as error:
                print(f"Error en producto #{numero}: {error}")
                continue
                
        return libros_pagina

    def _procesar_pagina(self, pagina):
        """Método interno equivalente a procesar_pagina() original con retries."""
        for intento in range(1, settings.MAX_RETRIES + 1):
            try:
                print(f"Intento {intento}/{settings.MAX_RETRIES}")
                # Esperar productos
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, settings.SELECTORS["producto"])))
                
                # Extraer
                libros = self._extraer_libros()
                
                if not libros:
                    raise WebDriverException("No se encontraron libros.")
                    
                print("   ✓ Página procesada correctamente.")
                return libros
                
            except TimeoutException:
                print(f"   Timeout en intento {intento}")
            except WebDriverException as error:
                print(f"   Error Selenium en intento {intento}: {error}")
                
            if intento < settings.MAX_RETRIES:
                print(f"   Esperando {settings.RETRY_DELAY} segundos...")
                time.sleep(settings.RETRY_DELAY)
                
        print(f"   Página {pagina} falló definitivamente.")
        return None

    def ejecutar_scraping(self):
        """Método principal que orquesta la paginación."""
        self.driver.get(self.url)
        pagina = 1

        while True:
            print(f"\n Página {pagina}")
            
            libros = self._procesar_pagina(pagina)
            
            if libros is None:
                self.errores.append({
                    "pagina": pagina,
                    "url": self.driver.current_url,
                    "error": "Falló después de 3 intentos"
                })
            else:
                self.datos.extend(libros)
                
            # Buscar el botón Next
            botones_next = self.driver.find_elements(By.CSS_SELECTOR, settings.SELECTORS["siguiente"])
            
            if not botones_next:
                print("\n✓ Última página alcanzada.")
                break
                
            # Click Next con retry
            click_exitoso = False
            for intento in range(1, 4):
                try:
                    print(f"   → Click Next (intento {intento}/3)")
                    botones_next[0].click()
                    click_exitoso = True
                    break
                except WebDriverException as error:
                    print(f"   Error haciendo click: {error}")
                    if intento < 3:
                        time.sleep(settings.RETRY_DELAY)
                        
            if not click_exitoso:
                self.errores.append({
                    "pagina": pagina,
                    "url": self.driver.current_url,
                    "error": "No se pudo hacer click en Next"
                })
                print(" No se pudo avanzar. Finalizando.")
                break
                
            pagina += 1

    def cerrar_cliente(self):
        """Cierra el navegador."""
        if self.driver:
            print("Cerrando navegador...")
            self.driver.quit()