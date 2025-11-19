from flask import Flask, redirect, url_for, session, request, g
from config import Config
from collections.abc import Mapping
import os
from werkzeug.security import generate_password_hash
# Importación de Blueprints
from login import login_bp, logout_bp, mysql
from routes import crud_bp, homepage_bp, good_bp, send_bp, reporturl_bp
from crud import (listcrud_bp, adduser_bp, listworker_bp, disable_user_bp,
                  disable_bp, edit_user_bp, enable_user_bp, report_bp,
                  ver_usuario_bp, add_student_bp, shedule_bp, add_grade_bp, dashboard_bp)
from administration import pending_excuses_bp, accept_excuse_bp, rejected_excuses_bp
from teacher import teacher_excuses_bp
from user import (excuse_bp, record_bd, get_estudents_bp, profile_bp,
                  assistant_bp, edit_profile_bp, contact_bp, recover_bp)
from notification import notification_bp


class GESDEApp:
    def __init__(self):
        self.app = Flask(
            __name__,
            template_folder=self.get_path('templates'),
            static_folder=self.get_path('static')
        )
        self.configure_app()
        self.register_blueprints()
        self.register_hooks()
        self.ensure_admin_user()

    def get_path(self, folder_name):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_dir, folder_name)

    def configure_app(self):
        self.app.config.from_object(Config)
        self.app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        self.app.config['SECRET_KEY'] = Config.SECRET_KEY
        mysql.init_app(self.app)

    def register_blueprints(self):
        app = self.app
        gesde_prefix = '/GESDE'

        # Login y logout
        app.register_blueprint(login_bp)
        app.register_blueprint(logout_bp, url_prefix=gesde_prefix)
        app.register_blueprint(send_bp, url_prefix=gesde_prefix)

        # CRUD
        for bp in [dashboard_bp, crud_bp, adduser_bp, add_student_bp, edit_user_bp,
                   listworker_bp, listcrud_bp, disable_user_bp, disable_bp, enable_user_bp,
                   report_bp, reporturl_bp, ver_usuario_bp, shedule_bp, add_grade_bp]:
            app.register_blueprint(bp, url_prefix=gesde_prefix)

        # Usuario
        for bp in [excuse_bp, homepage_bp, good_bp, record_bd, get_estudents_bp,
                   profile_bp, assistant_bp, notification_bp, edit_profile_bp,
                   contact_bp, recover_bp]:
            app.register_blueprint(bp, url_prefix=gesde_prefix)

        # Administración
        for bp in [pending_excuses_bp, accept_excuse_bp, rejected_excuses_bp]:
            app.register_blueprint(bp, url_prefix=gesde_prefix)

        # Profesor
        app.register_blueprint(teacher_excuses_bp, url_prefix=gesde_prefix)

    def register_hooks(self):
        app = self.app

        @app.route('/')
        def index():
            return redirect(url_for('login.login'))

        @app.context_processor
        def inject_grados():
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT grade FROM grade
                ORDER BY 
                CAST(SUBSTRING(grade, 1, LENGTH(grade)-1) AS UNSIGNED), 
                RIGHT(grade, 1);
            """)
            grados = cursor.fetchall()
            cursor.close()
            return dict(grados=grados)

        @app.context_processor
        def inject_session():
            usuario = {
                "id": session.get("user_id"),
                "name": session.get("name"),
                "rol": session.get("rol"),
                "idcard": session.get("usuario"),
                "phone": session.get("phone"),
                "last_updated": session.get("last_updated")
            }
            return dict(usuario=usuario)

        @app.before_request
        def verificar_sesion():
            rutas_publicas = [
                'login.login', 'static',
                'terminos_y_condiciones.send_pdf',
                'recover.recover', 'recover.recover_confirm',
                'recover.recover_password', 'user/recover_password'
            ]
            if 'usuario' not in session and request.endpoint not in rutas_publicas:
                return redirect(url_for('login.login'))

        @app.before_request
        def cargar_usuario_en_g():
            user_id = session.get('user_id')
            if user_id:
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                cursor.close()
                
                if row:
                    g.usuario = row if isinstance(row, Mapping) else {
                        'id': row[0], 'nombre': row[1], 'telefono': row[2],
                        'cedula': row[3], 'rol': row[4], 'password': row[5],
                        'profile_pic': row[6] or 'ASSETS/IMG/GenericImg/usuario.png'
                    }
                else:
                    g.usuario = None
            else:
                g.usuario = None

        @app.after_request
        def no_cache(response):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

    def ensure_admin_user(self):
        with self.app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT COUNT(*) AS total FROM users")
            result = cursor.fetchone()
            cursor.close()

            if result and result['total'] == 0:
                # No hay usuarios, creamos admin
                cursor = mysql.connection.cursor()
                hashed_password = generate_password_hash('admin123')
                profile_pic = 'ASSETS/IMG/GenericImg/usuario.png'  # Usa tu imagen por defecto

                cursor.execute("""
                    INSERT INTO users (name, rol, phone, idcard, password, profile_pic)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, ('admin', 'admin', '', '000-0000000-0', hashed_password, profile_pic))
                mysql.connection.commit()
                cursor.close()
                print("[INFO] Usuario administrador creado automáticamente.")


    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == "__main__":
    GESDEApp().run()