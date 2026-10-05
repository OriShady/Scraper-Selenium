# sources/books_bs4.py

import requests
from bs4 import BeautifulSoup
import time

from core.base_source import BaseScraper
from config import settings

class BS4Scraper(BaseScraper):
    def __init__(self, url=settings.BASE_URL):
        super().__init__(url)
        self.session = None

    def configurar_cliente(self):
        # Inicializa la sesion de requests.
        print("Iniciando conexion HTTP...")
        self.session = requests.Session()

    def _extraer_libros(self, html):
        # Analiza el DOM y extrae los datos de los elementos especificados.
        soup = BeautifulSoup(html, 'html.parser')
        productos = soup.select(settings.SELECTORS["producto"])
        libros_pagina = []

        print(f"   Productos encontrados: {len(productos)}")

        for numero, producto in enumerate(productos, start=1):
            try:
                titulo_elem = producto.select_one(settings.SELECTORS["titulo"])
                nombre = titulo_elem.get('title')
                url = titulo_elem.get('href')

                precio_elem = producto.select_one(settings.SELECTORS["precio"])
                precio = precio_elem.text

                rating_elem = producto.select_one(settings.SELECTORS["rating"])
                rating = rating_elem.get('class')[-1]

                libros_pagina.append({
                    "nombre": nombre,
                    "precio": precio,
                    "rating": rating,
                    "url": url
                })
            except Exception as error:
                print(f"   Error en producto #{numero}: {error}")
                continue

        return libros_pagina

    def ejecutar_scraping(self):
        # Controla la paginacion y ejecuta la extraccion secuencial.
        pagina = 1

        while True:
            print(f"\n Pagina {pagina}")

            if pagina == 1:
                url_pagina = self.url
            else:
                url_pagina = f"{self.url}/catalogue/page-{pagina}.html"

            try:
                response = self.session.get(url_pagina, timeout=settings.SELENIUM_TIMEOUT)
                response.encoding = 'utf-8'
                
                if response.status_code == 404:
                    print("Ultima pagina alcanzada.")
                    break

                response.raise_for_status()

                libros = self._extraer_libros(response.text)

                if not libros:
                    break

                self.datos.extend(libros)

                soup = BeautifulSoup(response.text, 'html.parser')
                siguiente = soup.select(settings.SELECTORS["siguiente"])

                if not siguiente:
                    print("Ultima pagina alcanzada.")
                    break

                pagina += 1
                time.sleep(1)

            except Exception as error:
                self.errores.append({
                    "pagina": pagina,
                    "url": url_pagina,
                    "error": str(error)
                })
                print(f"Error en extraccion: {error}")
                break

    def cerrar_cliente(self):
        # Cierra la sesion HTTP activa.
        if self.session:
            print("Cerrando conexion...")
            self.session.close()