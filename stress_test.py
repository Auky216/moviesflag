import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configuración
BASE_URL = "http://127.0.0.1:5000/api/movies"
SEARCH_TERMS = ["transformers", "batman", "spiderman", "avatar", "titanic"]  # Términos de búsqueda simulados
NUMBER_OF_REQUESTS = 100  # Número total de solicitudes a realizar
CONCURRENT_WORKERS = 20  # Número de hilos concurrentes

def send_request(search_term, page):
    """Envía una solicitud GET a la API con un término de búsqueda y un número de página."""
    try:
        response = requests.get(BASE_URL, params={"filter": search_term, "page": page})
        if response.status_code == 200:
            return f"Success: {search_term} - Page {page}"
        else:
            return f"Failed: {search_term} - Page {page} (Status: {response.status_code})"
    except Exception as e:
        return f"Error: {search_term} - Page {page} ({str(e)})"

def stress_test():
    """Realiza una prueba de estrés enviando múltiples solicitudes concurrentes."""
    print(f"Starting stress test with {NUMBER_OF_REQUESTS} requests and {CONCURRENT_WORKERS} workers...\n")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        # Crear tareas de prueba para cada solicitud
        futures = [
            executor.submit(send_request, term, page)
            for term in SEARCH_TERMS
            for page in range(1, (NUMBER_OF_REQUESTS // len(SEARCH_TERMS)) + 1)
        ]

        # Recoger resultados
        for future in as_completed(futures):
            print(future.result())

    end_time = time.time()
    print(f"\nStress test completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    stress_test()
