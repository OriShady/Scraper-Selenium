from ui.menu import mostrar_menu
from sources.books_selenium import SeleniumScraper
from database.db_manager import CSVManager

def main():
    opcion = mostrar_menu()

    if opcion == '1':
        print("\nIniciando extracción con Selenium...")
        scraper = SeleniumScraper()
    elif opcion == '2':
        print("\nVersión de BeautifulSoup aún no implementada.")
        return
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
            manager = CSVManager(scraper.datos, scraper.errores)
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