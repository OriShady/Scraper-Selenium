from ui.menu import mostrar_menu
from sources.books_selenium import SeleniumScraper
from database.db_manager import CSVManager
from sources.books_bs4 import BS4Scraper

def main():
    opcion = mostrar_menu()

    if opcion == '1':
        print("\nIniciando extracción con Selenium...")
        scraper = SeleniumScraper()
        prefijo = "selenium"
    elif opcion == '2':
        print("\nIniciando extracción con BeautifulSoup...")
        scraper = BS4Scraper()
        prefijo = "bs4"
    else:
        print("\nSaliendo del programa...")
        return

    try:
        # 1. Levantar el navegador
        scraper.configurar_cliente()
        
        # 2. Ejecutar la navegación y extracción de datos
        scraper.ejecutar_scraping()
        
        # 3. Procesar y guardar resultados en CSV
        if scraper.datos or scraper.errores:
            manager = CSVManager(scraper.datos, scraper.errores, prefijo)
            manager.procesar_y_guardar()
        else:
            print("\nNo se extrajeron datos para guardar.")
            
    except Exception as error:
        print(f"\nOcurrió un error inesperado en el sistema: {error}")
        
    finally:
        # 4. Cerrar Chrome siempre
        scraper.cerrar_cliente()

if __name__ == "__main__":
    main()