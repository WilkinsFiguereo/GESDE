class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Wilkins_12009'
    MYSQL_DB = 'GESDE'
    MYSQL_PORT = 3306
    SECRET_KEY = 'SECRET_KEY'

    # Método estático para conectar a la base de datos.
    @staticmethod
    def conectar():
        import MySQLdb  # O usa el conector que prefieras.
        try:
            # Conectamos a la base de datos MySQL usando los parámetros de la clase.
            connection = MySQLdb.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT
            )
            return connection  # Regresamos la conexión.
        except MySQLdb.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None
