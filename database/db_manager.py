import pandas as pd
from config import settings

class CSVManager:
    def __init__(self, datos, errores):
        self.datos = datos
        self.errores = errores

    def procesar_y_guardar(self):
        """Limpia los datos y los exporta a archivos CSV."""
        df = pd.DataFrame(self.datos)
        
        # Limpieza de datos (igual que en el script original)
        if not df.empty:
            # Limpiar precio
            df["precio"] = (
                df["precio"]
                .str.replace("£", "", regex=False)
                .astype(float)
            )
            
            # Convertir rating de texto a número usando nuestro settings
            df["rating"] = df["rating"].map(settings.RATINGS)

        # Crear DataFrame de errores
        df_errores = pd.DataFrame(self.errores)

        # Imprimir resultados en consola
        print("\n")
        print("=" * 60)
        print("SCRAPING TERMINADO")
        print("=" * 60)
        print(f"Libros obtenidos: {len(df)}")
        print(f"Páginas/operaciones con error: {len(df_errores)}")

        # Exportar datos a CSV
        df.to_csv("books.csv", index=False, encoding="utf-8")
        print("\n✓ books.csv creado.")

        # Exportar errores a CSV
        if not df_errores.empty:
            df_errores.to_csv("errores.csv", index=False, encoding="utf-8")
            print("✓ errores.csv creado.")
        else:
            print("✓ No hubo errores.")