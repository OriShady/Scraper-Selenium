from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, url):
        self.url = url
        self.datos = []
        self.errores = []

    @abstractmethod
    def configurar_cliente(self):
        """Inicializa el navegador o la sesión HTTP."""
        pass

    @abstractmethod
    def ejecutar_scraping(self):
        """Contiene la lógica de extracción y paginación."""
        pass

    @abstractmethod
    def cerrar_cliente(self):
        """Cierra conexiones o navegadores."""
        pass