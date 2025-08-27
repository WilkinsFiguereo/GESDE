class Config:
    # Definimos los parámetros de configuración dentro de la clase.
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Wilkins_12009'  # Cambia si es necesario
    MYSQL_DB = 'GESDE'  # Cambia por el nombre de tu base de datos
    MYSQL_PORT = 3307  # Si utilizas un puerto diferente, asegúrate de configurarlo aquí
    SECRET_KEY = 'SECRET_KEY'  # Asegúrate de tener una clave secreta para las sesiones de Flask
    
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
