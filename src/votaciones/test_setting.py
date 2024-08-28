import psycopg2
from testcontainers.postgres import PostgresContainer
from src.votaciones.settings import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DATABASE,
)
SCRIPT_PATH = '../../deploy/init-postgres.sql'

# Crea el contenedor con la imagen de PostgreSQL
postgres = PostgresContainer("postgres:13")

# Configura las variables de entorno para el usuario, la contraseña y la base de datos
postgres.with_env('POSTGRES_USER', POSTGRES_USER)
postgres.with_env('POSTGRES_PASSWORD', POSTGRES_PASSWORD)
postgres.with_env('POSTGRES_DB', POSTGRES_DATABASE)

# Inicia el contenedor
postgres.start()

# Obtén la URL de conexión para el contenedor
db_host = postgres.get_container_host_ip()
db_port = postgres.get_exposed_port(5432)

print(db_host, db_port)

# Conéctate a la base de datos y ejecuta el script SQL
try:
    # Conectar a la base de datos
    conn = psycopg2.connect(
        dbname=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=db_host,
        port=db_port
    )
    cursor = conn.cursor()

    # Leer y ejecutar el script SQL
    with open(SCRIPT_PATH, 'r') as sql_file:
        sql_script = sql_file.read()
        cursor.execute(sql_script)

    # Confirmar los cambios
    conn.commit()
    print("Script SQL ejecutado correctamente")

except Exception as e:
    print(f"Error al ejecutar el script SQL: {e}")

finally:
    # Cerrar la conexión a la base de datos
    if cursor:
        cursor.close()
    if conn:
        conn.close()
