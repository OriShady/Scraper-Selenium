# URL objetivo
BASE_URL = "https://books.toscrape.com"

# Configuraciones de comportamiento
SELENIUM_TIMEOUT = 20
MAX_RETRIES = 3
RETRY_DELAY = 2

# Selectores CSS centralizados
SELECTORS = {
    "producto": ".product_pod",
    "titulo": "h3 a",
    "precio": ".price_color",
    "rating": ".star-rating",
    "siguiente": ".next a"
}

# Mapeo de calificaciones a números
RATINGS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}