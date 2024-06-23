import sqlite3

# Conectar a la base de datos (se creará un archivo incendios.db en tu directorio de trabajo)
conn = sqlite3.connect('incendios.db')
cursor = conn.cursor()

# Crear una tabla para almacenar los datos
cursor.execute('''
CREATE TABLE IF NOT EXISTS incendios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    n_parte INTEGER,
    latitud REAL,
    longitud REAL,
    dia INTEGER,
    mes INTEGER,
    año INTEGER,
    hora INTEGER,
    minuto INTEGER,
    segundo INTEGER,
    estado TEXT,
    descripcion TEXT
)
''')

conn.commit()
conn.close()

print("Base de datos y tabla creada exitosamente.")
