import requests
import json
import random

# Configuración de la API local de la biblioteca
BASE_URL = "http://library.demo.local/api/v1"
AUTH = ("cisco", "cisco123!")

def consultar_y_ordenar_catalogo():
    print("=== CONSULTANDO CATÁLOGO DE LA BIBLIOTECA ===")
    url = f"{BASE_URL}/books"
    
    try:
        response = requests.get(url, auth=AUTH, timeout=5)
        if response.status_code == 200:
            libros = response.json()
            
            # Ordenar alfabéticamente por el campo 'author'
            libros_ordenados = sorted(libros, key=lambda x: x.get('author', '').lower())
            
            print(f"\nTotal de libros encontrados: {len(libros_ordenados)}\n")
            print(f"{'AUTOR':<30} | {'TÍTULO':<40} | {'ISBN':<15}")
            print("-" * 90)
            
            for libro in libros_ordenados:
                autor = libro.get('author', 'N/A')
                titulo = libro.get('title', 'N/A')
                isbn = libro.get('isbn', 'N/A')
                print(f"{autor:<30} | {titulo:<40} | {isbn:<15}")
        else:
            print(f"Error al obtener libros. Código HTTP: {response.status_code}")
    except Exception as e:
        print(f"Error de conexión: {e}")

def agregar_libros_aleatorios(cantidad=50):
    print(f"\n=== INSERTANDO {cantidad} LIBROS ALEATORIOS ===")
    url = f"{BASE_URL}/books"
    headers = {"Content-Type": "application/json"}
    
    autores = ["Gabriel Garcia Marquez", "Isabel Allende", "Jorge Luis Borges", "Pablo Neruda", "Mario Vargas Llosa"]
    generos = ["Novela", "Ficcion", "Poesia", "Historia", "Ensayo"]
    
    exitosos = 0
    for i in range(1, cantidad + 1):
        nuevo_libro = {
            "title": f"Libro Automatizado {random.randint(100, 999)}",
            "author": random.choice(autores),
            "isbn": f"978-{random.randint(1000, 9999)}-{random.randint(10, 99)}",
            "genre": random.choice(generos)
        }
        
        try:
            res = requests.post(url, auth=AUTH, headers=headers, data=json.dumps(nuevo_libro), timeout=3)
            if res.status_code in [200, 201]:
                exitosos += 1
        except Exception:
            pass

    print(f"Proceso completado. Libros agregados con éxito: {exitosos}/{cantidad}")

if __name__ == "__main__":
    consultar_y_ordenar_catalogo()
    agregar_libros_aleatorios(50)
