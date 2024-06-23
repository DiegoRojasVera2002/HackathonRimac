import sqlite3

conn = sqlite3.connect('incendios.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(incendios)")
columns = [info[1] for info in cursor.fetchall()]
if 'riesgo1' not in columns:
    cursor.execute("ALTER TABLE incendios ADD COLUMN riesgo1 INTEGER")
if 'riesgo2' not in columns:
    cursor.execute("ALTER TABLE incendios ADD COLUMN riesgo2 INTEGER")

cursor.execute(
    "SELECT id, latitud, longitud, distance1, distance2 FROM incendios")
rows = cursor.fetchall()

for row in rows:
    id = row[0]
    lat = row[1]
    lon = row[2]
    distance1 = row[3]
    distance2 = row[4]

    # Calcular si la distancia es menor a 1000 metros
    if distance1 < 2:  # 1 kilómetro = 1000 metros
        riesgo1 = 1
    else:
        riesgo1 = 0

    # También se puede usar un enfoque booleano
    riesgo2 = 1 if distance2 < 2 else 0

    cursor.execute(
        "UPDATE incendios SET riesgo1 = ?, riesgo2 = ? WHERE id = ?", (riesgo1, riesgo2, id))

conn.commit()
conn.close()

print("Actualización completada.")
