def mostrar_menu():
    print("\n" + "=" * 45)
    print("SCRAPER DE LIBROS ")
    print("=" * 45)
    print("1. Extraccion con Selenium")
    print("2. Extraccion con BeautifulSoup")
    print("3. Salir")
    print("=" * 45)
    
    while True:
        opcion = input("Selecciona una herramienta (1-3): ")
        if opcion in ['1', '2', '3']:
            return opcion
        print("Opción no válida. Intenta de nuevo.")