import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import googlemaps
from bs4 import BeautifulSoup
import re
import sqlite3
import random
import time
from datetime import datetime

# Conectar a la base de datos
conn = sqlite3.connect('incendios.db')
cursor = conn.cursor()

# Eliminar datos existentes
cursor.execute('DELETE FROM incendios')
conn.commit()

# Reiniciar el contador de ID (sqlite_sequence)
cursor.execute('DELETE FROM sqlite_sequence WHERE name = "incendios"')
conn.commit()

# API_key de Google Maps:
API_KEY = 'AIzaSyDl4YDAOuhZT4IjMaa-aHpnDsoA8qkbNZY'

# Crear un cliente de Google Maps (Yo):
gmaps = googlemaps.Client(key=API_KEY)

# Website - Incendios:
url = "https://sgonorte.bomberosperu.gob.pe/24horas"

# Configurar undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = uc.Chrome(options=options)

# Navegar a la página web
driver.get(url)
# Esperar a que la página se cargue completamente
time.sleep(random.uniform(2, 5))

# Obtener el contenido de la página
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Cerrar el navegador de manera segura
try:
    if driver:
        driver.quit()
except Exception as e:
    print(f"Error al cerrar el navegador: {e}")
driver.quit()

alertas = soup.find_all('div', class_='card shadow mt-2 mb-2 bg-danger')

for alerta in alertas:
    n_parte = int(re.search(
        r'\d+', alerta.find('p', class_='card-text m-0 mb-2').text.strip()).group())

    estado = alerta.find('h6', class_='card-title text-warning').text.strip()
    descripcion = re.sub(r'^\s*#\d+\s*', '',
                         alerta.find('h5', class_='card-title').text.strip())

    direccion = alerta.find_all('p', class_='card-text m-0')[0].text.strip()

    # Verificar que la lista de 'p' tenga al menos dos elementos
    p_tags = alerta.find_all('p', class_='card-text m-0')
    if len(p_tags) > 1:
        fecha_hora = p_tags[1].text.strip()

        # Limpiar la fecha y hora para eliminar el icono
        fecha_hora = re.sub(r'<i.*?</i>', '', fecha_hora).strip()

        if fecha_hora:
            # Replace 'a.m.' and 'p.m.' with 'AM' and 'PM'
            fecha_hora = fecha_hora.replace('a.m.', 'AM').replace('p.m.', 'PM')

            # Convertir la fecha y hora a un objeto datetime
            formato = "%d/%m/%Y %I:%M:%S %p"
            fecha_hora_dt = datetime.strptime(fecha_hora, formato)

            # Extraer los componentes individuales
            dia = fecha_hora_dt.day
            mes = fecha_hora_dt.month
            año = fecha_hora_dt.year
            hora = fecha_hora_dt.hour
            minuto = fecha_hora_dt.minute
            segundo = fecha_hora_dt.second

        if direccion:
            # Proceso de geocodificación:
            try:
                resultado_geo = gmaps.geocode(direccion)

                # Extraer la latitud y longitud si se encontró un resultado
                if resultado_geo:
                    location = resultado_geo[0]['geometry']['location']
                    latitud = location['lat']
                    longitud = location['lng']

                    # Insertar los datos en la base de datos
                    cursor.execute('''
                    INSERT INTO incendios (n_parte, latitud, longitud, dia, mes, año, hora, minuto, segundo, estado, descripcion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (n_parte, latitud, longitud, dia, mes, año, hora, minuto, segundo, estado, descripcion))

                    conn.commit()
                else:
                    print(
                        f'No se encontraron resultados para la dirección: {direccion}')

            except googlemaps.exceptions.ApiError as e:
                print(f'Error al llamar a la API de Google Maps: {e}')
            except Exception as e:
                print(f'Ocurrió un error: {e}')

    tiempo_espera = random.uniform(1, 2)
    time.sleep(tiempo_espera)

# Cerrar la conexión a la base de datos
conn.close()
