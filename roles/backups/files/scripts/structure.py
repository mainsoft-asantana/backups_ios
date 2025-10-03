import psycopg2
from vars import DATABASE, HOST, PASSWORD, PORT, USER

host = str(HOST)
port = str(PORT)
database = str(DATABASE)
user = str(USER)
password = str(PASSWORD)


class PostgresStructure:
    def __init__(self):
        self.connection_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }

    def create_tables(self):
        try:
            # Crear la conexión a PostgreSQL
            conexion: Any = psycopg2.connect(**self.connection_params)  # type: ignore
            cursor = conexion.cursor()

            create_tables = """
                CREATE TABLE IF NOT EXISTS system (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150),
                        state BOOLEAN DEFAULT TRUE,
                        UNIQUE (name)
                    );

                CREATE TABLE IF NOT EXISTS inventory (
                        id SERIAL PRIMARY KEY,
                        number_ip VARCHAR(150) UNIQUE,
                        state BOOLEAN DEFAULT TRUE
                    );

                CREATE TABLE IF NOT EXISTS version (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) UNIQUE,
                    state BOOLEAN DEFAULT TRUE
                );

                CREATE TABLE IF NOT EXISTS model (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) UNIQUE,
                    state BOOLEAN DEFAULT TRUE
                );

                CREATE TABLE IF NOT EXISTS type (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) UNIQUE,
                    state BOOLEAN DEFAULT TRUE
                );

                CREATE TABLE IF NOT EXISTS hostname (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) UNIQUE,
                    state BOOLEAN DEFAULT TRUE
                );

                CREATE TABLE IF NOT EXISTS backups (
                    id SERIAL PRIMARY KEY,

                    system_id INTEGER,
                    inventory_id INTEGER,
                    version_id INTEGER,
                    model_id INTEGER,
                    type_id INTEGER,
                    hostname_id INTEGER,

                    created_at DATE DEFAULT CURRENT_DATE,
                    backups TEXT,
                    state BOOLEAN DEFAULT TRUE,

                    FOREIGN KEY (system_id) REFERENCES system(id) ON DELETE CASCADE,
                    FOREIGN KEY (inventory_id) REFERENCES inventory(id) ON DELETE CASCADE,
                    FOREIGN KEY (version_id) REFERENCES version(id) ON DELETE CASCADE,
                    FOREIGN KEY (model_id) REFERENCES model(id) ON DELETE CASCADE,

                    FOREIGN KEY (type_id) REFERENCES type(id) ON DELETE CASCADE,
                    FOREIGN KEY (hostname_id) REFERENCES hostname(id) ON DELETE CASCADE,

                    UNIQUE (system_id, inventory_id, version_id, model_id, type_id, hostname_id, created_at)
                );


            """
            create_views_backups = """
               CREATE OR REPLACE VIEW vw_backups AS
                SELECT
                    d.id AS device_id,
                    s.name AS system_name,
                    i.number_ip AS inventory_ip,
                    v.name AS version_name,
                    m.name AS model_name,
                    t.name AS type_name,
                    h.name AS hostname_name,
                    d.created_at,
                    d.backups,
                    d.state
                FROM backups d
                LEFT JOIN system s ON d.system_id = s.id
                LEFT JOIN inventory i ON d.inventory_id = i.id
                LEFT JOIN version v ON d.version_id = v.id
                LEFT JOIN model m ON d.model_id = m.id
                LEFT JOIN type t ON d.type_id = t.id
                LEFT JOIN hostname h ON d.hostname_id = h.id;
            """

            cursor.execute(create_tables)
            cursor.execute(create_views_backups)
            conexion.commit()

            print("Tablas creadas o verificadas correctamente.")

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error al crear las tablas: {error}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()