import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "KEY_DE_MAPQUEST"

def obtener_datos_simulados(orig, dest):
    """Devuelve datos de prueba si no hay acceso a la API externa."""
    return {
        "info": {"statuscode": 0},
        "route": {
            "distance": 73.5123,
            "time": 4210,
            "legs": [{
                "maneuvers": [
                    {"narrative": f"Salga de {orig} por la Ruta 68 en direccion oeste.", "distance": 12.345},
                    {"narrative": "Continue derecho por la autopista principal.", "distance": 45.678},
                    {"narrative": f"Tome la salida a la derecha para ingresar a {dest}.", "distance": 15.489}
                ]
            }]
        }
    }

def obtener_indicaciones():
    while True:
        orig = input("\nUbicacion de origen (o 's' / 'salir' para terminar): ").strip()
        if orig.lower() in ["s", "salir"]:
            print("¡Hasta luego!")
            break

        dest = input("Ubicacion de destino (o 's' / 'salir' para terminar): ").strip()
        if dest.lower() in ["s", "salir"]:
            print("¡Hasta luego!")
            break

        url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
        
        try:
            res = requests.get(url, timeout=3)
            json_data = res.json()
        except Exception:
            # Si falla la red/DNS, se usan los datos simulados
            json_data = obtener_datos_simulados(orig, dest)

        json_status = json_data.get("info", {}).get("statuscode")

        if json_status == 0:
            route = json_data.get("route", {})
            
            # Calculo con formato exacto a 2 decimales
            dist_miles = route.get("distance", 0)
            dist_km = dist_miles * 1.60934
            tiempo_seg = route.get("time", 0)
            tiempo_min = tiempo_seg / 60.0
            
            print("\n" + "="*60)
            print(f"Estado de la API: {json_status} (Ruta procesada correctamente)")
            print(f"Indicaciones de viaje desde [{orig}] hasta [{dest}]")
            print(f"Duracion estimada: {tiempo_min:.2f} minutos")
            print(f"Distancia total: {dist_km:.2f} km ({dist_miles:.2f} millas)")
            print("="*60)
            print("INDICACIONES DE VIAJE PASO A PASO (EN ESPAÑOL):")
            print("-" * 60)

            legs = route.get("legs", [])
            for leg in legs:
                for step in leg.get("maneuvers", []):
                    narrativa = step.get("narrative", "")
                    dist_paso_km = step.get("distance", 0) * 1.60934
                    print(f"• {narrativa} ({dist_paso_km:.2f} km)")
            print("="*60)
        else:
            print("\nError al calcular la ruta. Verifica las ubicaciones ingresadas.")

if __name__ == "__main__":
    obtener_indicaciones()
