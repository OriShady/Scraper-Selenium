import pandas as pd
from config import settings

class CSVManager:
    def __init__(self, datos, errores, prefijo):
        self.datos = datos
        self.errores = errores
        self.prefijo = prefijo

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
        archivo_datos = f"books_{self.prefijo}.csv" # agregar prefijo si es necesario
        df.to_csv(archivo_datos, index=False, encoding="utf-8")
        print(f"\n {archivo_datos} creado.")

        # Exportar errores a CSV
        if not df_errores.empty:
            archivo_errores = f"errores_{self.prefijo}.csv"
            df_errores.to_csv(archivo_errores, index=False, encoding="utf-8")
            print(f" {archivo_errores} creado.")
        else:
            print(" No hubo errores.")