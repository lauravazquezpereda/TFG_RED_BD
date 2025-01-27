import sqlite3

def create_database(video_name):
    # Conectar o crear la base de datos
    conn = sqlite3.connect('emotions.db')  # Objeto de conexión que permite interactuar con la base de datos
    c = conn.cursor()  # Cursor para ejecutar comandos SQL en la base de datos

    # Generar el nombre de la tabla
    table_name = f"expressions_{video_name.replace('.', '_')}"

    # Crear la tabla con un comando SQL dinámico
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            timestamp REAL,
            emotion TEXT   
        )
    ''')
    
    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

    # Devolver el nombre de la tabla creada
    return table_name
