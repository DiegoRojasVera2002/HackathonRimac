import sqlite3
import json
import googlemaps


def generate_json_from_db():
    conn = sqlite3.connect('incendios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT latitud, longitud, descripcion FROM incendios')
    locations = cursor.fetchall()
    conn.close()

    # Convertir los resultados en un formato JSON
    data = [{'latitud': lat, 'longitud': lng, 'descripcion': title}
            for lat, lng, title in locations]

    # Escribir el JSON en un archivo
    with open('locations.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    generate_json_from_db()

# Reemplaza 'TU_API_KEY' con tu propia clave de API de Google Maps
api_key = 'AIzaSyDl4YDAOuhZT4IjMaa-aHpnDsoA8qkbNZY'
gmaps = googlemaps.Client(key=api_key)

try:
    # Obtener la ubicación actual del dispositivo
    current_location = gmaps.geolocate()

    # Extraer latitud y longitud
    lat_real = current_location['location']['lat']
    lng_real = current_location['location']['lng']

except Exception as e:
    print(f"No se pudo obtener la ubicación: {e}")


def calculate_distance(lat1, lon1, lat2, lon2):
    # Calcula la distancia utilizando la API de Google Maps
    origins = (lat1, lon1)
    destinations = (lat2, lon2)
    result = gmaps.distance_matrix(origins, destinations, mode='driving')
    # en kilómetros
    distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
    return distance


def update_database_with_distances(database_path, known_location):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verificar si la columna 'distance' ya existe, si no, agregarla
    cursor.execute("PRAGMA table_info(incendios)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'distance' not in columns:
        cursor.execute("ALTER TABLE incendios ADD COLUMN distance1 REAL")

    cursor.execute("SELECT id, latitud, longitud FROM incendios")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        lat = row[1]
        lon = row[2]
        distance = calculate_distance(
            known_location[0], known_location[1], lat, lon)

        cursor.execute(
            "UPDATE incendios SET distance1 = ? WHERE id = ?", (distance, id))

    conn.commit()
    conn.close()


def update_database_with_distances2(database_path, known_location):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verificar si la columna 'distance' ya existe, si no, agregarla
    cursor.execute("PRAGMA table_info(incendios)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'distance' not in columns:
        cursor.execute("ALTER TABLE incendios ADD COLUMN distance2 REAL")

    cursor.execute("SELECT id, latitud, longitud FROM incendios")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        lat = row[1]
        lon = row[2]
        distance = calculate_distance(
            known_location[0], known_location[1], lat, lon)

        cursor.execute(
            "UPDATE incendios SET distance2 = ? WHERE id = ?", (distance, id))

    conn.commit()
    conn.close()


# Ubicación fija conocida (latitud, longitud)
known_location = (lat_real, lng_real)  # Ejemplo: Lima, Perú
new_location = (-12.0295378, -77.0599784)

# Actualizar la base de datos con las distancias calculadas
update_database_with_distances('incendios.db', known_location)

# Actualizar la base de datos con las distancias calculadas
update_database_with_distances2('incendios.db', new_location)

print("Actualización completada.")
