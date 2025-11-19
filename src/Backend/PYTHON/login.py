from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash


# Inicialización de Blueprint
login_bp = Blueprint('login', __name__, template_folder='../templates')
logout_bp = Blueprint('logout', __name__)

mysql = MySQL()

class Database:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_connection(self):
        try:
            connection = self.mysql.connection
            return connection.cursor()
        except Exception as err:
            print(f"Error: {err}")
            return None


class User:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate(self, idcard, password):
        cursor = None
        try:
            cursor = self.db_connection.get_connection()
            cursor.execute("SELECT * FROM users WHERE idcard = %s", (idcard,))
            user = cursor.fetchone()

            if user and check_password_hash(user["password"], password):
                return user  # Autenticación exitosa
            else:
                return None  # Credenciales incorrectas

        except Exception as e:
            print(f"Error during authentication: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


    def set_session(self, user):
        session['usuario'] = user['idcard']
        session['rol'] = user['rol']
        session['name'] = user['name']
        session['phone'] = user['phone']
        session['user_id'] = user['id']
        session['last_updated'] = user['last_updated']


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        idcard = request.form.get('IDcard')
        password = request.form.get('Password')

        # Evita usar MySQL si no está inicializado (modo test)
        if not hasattr(mysql, 'connection'):
            flash('Base de datos no disponible en modo de prueba', 'error')
            return redirect(url_for('login.login'))

        db = Database(mysql)
        user_handler = User(db)
        usuario = user_handler.authenticate(idcard, password)
        if usuario:
            # Configurar la sesión
            user_handler.set_session(usuario)

            # Determinar destino según el rol
            if usuario['rol'] == 'admin':
                destino = url_for('dashboard.dashboard')
            elif usuario['rol'] == 'parent':
                destino = url_for('homepage.homepage')
            elif usuario['rol'] == 'administration':
                destino = url_for('pending.pending')
            elif usuario['rol'] == 'teacher':
                destino = url_for('teacher.show_excuses')
            else:
                destino = url_for('login.login')

            # Renderizar pantalla de carga con redirección automática
            return render_template('loading_screen.html', destino=destino)
        else:
            flash('Ups, algo salió mal. Revisa tus datos e inténtalo nuevamente.', 'error')
            return redirect(url_for('login.login'))  # Redirige a GET para evitar reenvío del formulario

    # En el caso GET, simplemente renderizamos la página de login.
    return render_template('login.html')


@logout_bp.route('/logout')
def logout():
    session.clear()  # Limpiar sesión
    return render_template('loading_screen.html', destino=url_for('login.login'))
