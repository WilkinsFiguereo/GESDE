from flask import render_template, request, redirect, url_for, Blueprint, jsonify, flash, send_file, current_app, make_response, session
from login import mysql
from fpdf import FPDF
import tempfile
from twilio.rest import Client
from datetime import datetime  
import math, tempfile
from werkzeug.security import generate_password_hash
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from pathlib import Path
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
import os

# Inicialización de Blueprints
adduser_bp = Blueprint('adduser', __name__, template_folder='../templates')
add_student_bp = Blueprint('addstudents', __name__, template_folder='../templates')
disable_user_bp = Blueprint('disable_user', __name__, template_folder='../templates')
edit_user_bp = Blueprint('edit_user', __name__, template_folder='../templates')
enable_user_bp = Blueprint('enable', __name__, template_folder='../templates')
listcrud_bp = Blueprint('listcrud', __name__, template_folder='../templates')
listworker_bp = Blueprint('listworker', __name__, template_folder='templates')
disable_bp = Blueprint('disable', __name__, template_folder='templates')
report_bp = Blueprint('report', __name__, template_folder='templates')
ver_usuario_bp = Blueprint('ver_usuario', __name__)
shedule_bp = Blueprint('shedule', __name__, template_folder='../templates')
add_grade_bp = Blueprint('addgrade', __name__, template_folder='../templates')
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')


class UserDatabase:
    def __init__(self, mysql_connection):
        self.mysql = mysql_connection

    def get_cursor(self):
        try:
            return self.mysql.connection.cursor()  # Usando Diccionario
        except Exception as e:
            print(f"Error al obtener el cursor: {e}")
            return None


    def inject_dashboard(self):
        try:
            cursor = self.mysql.connection.cursor()

            # === Totales generales ===
            cursor.execute("SELECT COUNT(*) AS total_excuses FROM pending_excuses")
            total_excuses = cursor.fetchone()["total_excuses"]

            cursor.execute("SELECT COUNT(*) AS total_accepted FROM accepted_excuses")
            total_accepted = cursor.fetchone()["total_accepted"]

            cursor.execute("SELECT COUNT(*) AS total_rejected FROM rejected_excuses")
            total_rejected = cursor.fetchone()["total_rejected"]

            # === Totales desde el lunes ===
            cursor.execute("""
                SELECT COUNT(*) AS week_excuses 
                FROM pending_excuses 
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)
            """)
            week_excuses = cursor.fetchone()["week_excuses"]

            cursor.execute("""
                SELECT COUNT(*) AS week_accepted 
                FROM accepted_excuses 
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)
            """)
            week_accepted = cursor.fetchone()["week_accepted"]

            cursor.execute("""
                SELECT COUNT(*) AS week_rejected 
                FROM rejected_excuses 
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)
            """)
            week_rejected = cursor.fetchone()["week_rejected"]
            
            # Conteo de usuarios por rol
            
            cursor.execute("SELECT COUNT(*) AS total_user FROM users")
            total_user = cursor.fetchone()["total_user"]
                 
            cursor.execute("SELECT COUNT(*) AS total_user FROM userunbailited")
            total_user_userunbailited = cursor.fetchone()["total_user"]
            
            cursor.execute("SELECT COUNT(*) AS total_user FROM students")
            total_students = cursor.fetchone()["total_user"]
 
            cursor.execute("SELECT rol, COUNT(*) AS total FROM users GROUP BY rol")
            roles_data = cursor.fetchall()
            total_admin = total_padre = total_profesor = total_otro = total_administration = 0
            for row in roles_data:
                rol = row["rol"].lower()
                if rol == "admin":
                    total_admin = row["total"]
                elif rol == "parent":
                    total_padre = row["total"]
                elif rol == "teacher":
                    total_profesor = row["total"]
                elif rol == "administration":
                    total_administration = row["total"]
                else:
                    total_otro += row["total"]  # para otros roles desconocidos
            
            #Mensajes
            
            cursor.execute("SELECT COUNT(*) AS menssage FROM contact")
            menssage = cursor.fetchone()["menssage"]
            return {
                    
                    'total_excuses': total_excuses,
                    'total_accepted': total_accepted,
                    'total_rejected': total_rejected,
                    'week_excuses': week_excuses,
                    'week_accepted': week_accepted,
                    'week_rejected': week_rejected,
                    'total_admin': total_admin,
                    'total_padre': total_padre,
                    'total_profesor': total_profesor,
                    'total_administration': total_administration,
                    'total_user': total_user,
                    'total_user_userunbailited': total_user_userunbailited,
                    'total_students': total_students,
                    'total_otro': total_otro,
                    'menssage': menssage
                }
                
        except Exception as e:
            print(f"Error al obtener los totales: {e}")
            return {
                'total_excuses': 0,
                'total_accepted': 0,
                'total_rejected': 0,
                'week_excuses': 0,
                'week_accepted': 0,
                'week_rejected': 0,
                'total_admin': 0,
                'total_padre': 0,
                'total_profesor': 0,
                'total_administration': 0,
                'total_user': 0,
                'total_user_userunbailited': 0,
                'total_otro': 0
            }
        finally:
            cursor.close()


    def insert_user(self, name, rol, phone, idcard, password, profile_pic):
        cursor = self.mysql.connection.cursor()
        # Cifrar la contraseña
        hashed_password = generate_password_hash(password)
        query = """
         INSERT INTO users (name, rol, phone, idcard, password, profile_pic)
         VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, rol, phone, idcard, hashed_password, profile_pic))
        self.mysql.connection.commit()
        cursor.close()

    def insert_students(self, name, grade):
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                INSERT INTO students (name, grade) 
                VALUES (%s, %s)
            """, (name, grade))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            self.mysql.connection.rollback()
        finally:
            if cursor:
                cursor.close()
                
    def delete_student(self, student_id):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            self.mysql.connection.commit()
        finally:
            cursor.close()
    
    def get_all_students(self):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("SELECT id, name, grade FROM students")
            return cursor.fetchall()
        finally:
            cursor.close()
    def insert_grade(self, grade):
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                INSERT INTO grade ( grade) 
                VALUES (%s)
            """, ( grade,))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            self.mysql.connection.rollback()
        finally:
            if cursor:
                cursor.close()
    def get_grades(self):
        
        cursor = None
        
        try:
            
            cursor = self.get_cursor()
            
            if not cursor:
            
             return []

            
            cursor.execute("SELECT id, grade FROM grade")
            
            return cursor.fetchall()
        
        except Exception as e:
            
            print(f"Error al obtener las calificaciones: {e}")
            
            return []
        
        finally:
            
            if cursor:
                
                cursor.close()
       
    def update_user(self, user_id, name, rol, phone, idcard, password=None):
        try:
            hashed_password = generate_password_hash(password)
            cursor = self.get_cursor()
            if password:
                cursor.execute('''UPDATE users 
                                  SET name = %s, idcard = %s, phone = %s, rol = %s, password = %s 
                                  WHERE id = %s''',
                               (name, idcard, phone, rol, hashed_password, user_id))
            else:
                cursor.execute('''UPDATE users 
                                  SET name = %s, idcard = %s, phone = %s, rol = %s 
                                  WHERE id = %s''',
                               (name, idcard, phone, rol, user_id))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            self.mysql.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    def get_users(self, condition='', params=None, table='users', limit=None, offset=None):
        cursor = None
        try:
            cursor = self.get_cursor()
            if not cursor:
                return []

            sql = f"SELECT * FROM `{table}` {condition}"
            all_params = params.copy() if params else []

            if limit is not None and offset is not None:
                sql += " LIMIT %s OFFSET %s"
                all_params += [limit, offset]

            cursor.execute(sql, all_params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
                
    def get_students(self, condition='', params=None, table='students', limit=None, offset=None):
        cursor = None
        try:
            cursor = self.get_cursor()
            if not cursor:
                return []

            sql = f"SELECT * FROM `{table}` {condition}"
            all_params = params.copy() if params else []

            if limit is not None and offset is not None:
                sql += " LIMIT %s OFFSET %s"
                all_params += [limit, offset]

            cursor.execute(sql, all_params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

        

    def count_users(self, condition='', params=None, table='users'):
        cursor = None
        try:
            cursor = self.get_cursor()
            if not cursor:
                return 0

            sql = f"SELECT COUNT(*) AS total FROM `{table}` {condition}"
            cursor.execute(sql, params or [])
            row = cursor.fetchone()
            return row['total'] if row else 0
        except Exception as e:
            print(f"Error al contar usuarios: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()


                
    def get_disabled_users(self, per_page=7, offset=0):
        try:
            cursor = self.get_cursor()
            query = "SELECT * FROM userunbailited LIMIT %s OFFSET %s"
            cursor.execute(query, (per_page, offset))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener usuarios deshabilitados: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def delete_user(self, user_id, table='users'):
        try:
            cursor = self.get_cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id = %s", (user_id,))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            self.mysql.connection.rollback()
        finally:
            if cursor:
                cursor.close()
                
    def delete_message(self, message_id):
        try:
            cursor = self.get_cursor()
            cursor.execute("DELETE FROM contact WHERE id_contact = %s", (message_id,))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al eliminar el mensaje: {e}")
            self.mysql.connection.rollback()
        finally:
            if cursor:
                cursor.close()
    
    def get_students_by_parent(self, parent_id):
        cursor = self.get_cursor()
        try:
            cursor.execute("""
                SELECT s.id, s.name, s.grade 
                FROM students s
                JOIN parent_student ps ON s.id = ps.student_id
                WHERE ps.parent_id = %s
            """, (parent_id,))
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
    
    def assign_student_to_parent(self, parent_id, student_id):
        cursor = self.get_cursor()
        try:
            # Verificar si la relación ya existe
            cursor.execute("SELECT 1 FROM parent_student WHERE parent_id = %s AND student_id = %s", 
                      (parent_id, student_id))
            if cursor.fetchone():
                return  # Ya existe la relación
            
            cursor.execute("""
                INSERT INTO parent_student (parent_id, student_id)
                VALUES (%s, %s)
            """, (parent_id, student_id))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al asignar estudiante: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
                
            
    def delete_parent_student_relations(self, parent_id):
        cursor = self.get_cursor()
        try:
            cursor.execute("DELETE FROM parent_student WHERE parent_id = %s", (parent_id,))
            self.mysql.connection.commit()
        finally:
            if cursor:
                cursor.close()
       
    def get_connection(self):
        return self.mysql.connection
    
    def get_available_grades(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT grade FROM students ORDER BY grade")
            grades = [row['grade'] for row in cursor.fetchall()]
            return grades
        finally:
            cursor.close()
    
    def count_students(self, condition=None, params=None):
        cursor = self.get_cursor()
        query = "SELECT COUNT(*) AS total FROM students"  # 👈 Aquí inicializamos la query

        if condition:
            # Elimina 'WHERE' si lo trae por error desde afuera
            if condition.strip().lower().startswith("where"):
                condition = condition[5:].strip()
            query += " WHERE " + condition

        if params is None:
            params = ()

        cursor.execute(query, params)
        row = cursor.fetchone()
        return row['total'] if row else 0




    
    def get_students(self, condition=None, params=None, limit=10, offset=0):
        cursor = self.get_cursor()
        query = "SELECT * FROM students"

        if condition:
            # Elimina 'WHERE' si lo trae por error desde afuera
            if condition.strip().lower().startswith("where"):
                condition = condition[5:].strip()
            query += " WHERE " + condition

        query += " LIMIT %s OFFSET %s"

        if params is None:
            params = []

        if isinstance(params, tuple):
            params = list(params)

        cursor.execute(query, params + [limit, offset])
        return cursor.fetchall()


class ScheduleDatabase:
    def __init__(self, mysql_connection):
        self.mysql = mysql_connection

    def get_cursor(self):
        try:
            return self.mysql.connection.cursor()
        except Exception as e:
            print(f"Error al obtener cursor: {e}")
            return None

    def insert_schedule(self, teacher_id, day_of_week, grade):
        cursor = self.get_cursor()
        try:
            sql = """
            INSERT INTO teacher_schedule (teacher_id, day_of_week, grade)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (teacher_id, day_of_week, grade))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al insertar horario: {e}")
            self.mysql.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    def get_all_teachers(self):
        cursor = self.get_cursor()
        try:
            sql = "SELECT id, name FROM users WHERE rol = 'teacher'"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener profesores: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
                
    def unassign_grade(self, teacher_id, grade):
        cursor = self.get_cursor()
        try:
            sql = """
            DELETE FROM teacher_schedule
            WHERE teacher_id = %s AND grade = %s
            """
            cursor.execute(sql, (teacher_id, grade))
            self.mysql.connection.commit()
        except Exception as e:
            print(f"Error al desasignar grado: {e}")
            self.mysql.connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
    def get_assigned_grades(self, teacher_id):
        cursor = self.get_cursor()
        try:
            sql = """
            SELECT grade FROM teacher_schedule
            WHERE teacher_id = %s
            """
            cursor.execute(sql, (teacher_id,))
            return [row['grade'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener grados asignados: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

class UpdateController:
    def __init__(self, mysql):
        self.mysql = mysql

    def register(self, type, detail):
        cursor = self.mysql.connection.cursor()
        query = "INSERT INTO update_notification (type, detail) VALUES (%s, %s)"
        cursor.execute(query, (type, detail))
        self.mysql.connection.commit()
        cursor.close()

@dashboard_bp.route('/dashboard')
def dashboard():
    user_db = UserDatabase(mysql)
    dashboard_data = user_db.inject_dashboard()

    cursor = mysql.connection.cursor()

    # Últimas actualizaciones
    cursor.execute("SELECT * FROM update_notification ORDER BY date DESC LIMIT 4")
    updates = cursor.fetchall()

    # Últimos mensajes
    
    cursor.execute("SELECT * FROM contact ")
    menssages_complet = cursor.fetchall()
    
    cursor.execute("SELECT * FROM contact ORDER BY date DESC LIMIT 3")
    menssages = cursor.fetchall()

    # Total de mensajes
    cursor.execute("SELECT COUNT(*) FROM contact")
    total_menssages = cursor.fetchone()['COUNT(*)']


    cursor.close()

    return render_template(
        'crud/dashboard.html',
        **dashboard_data,
        updates=updates,
        menssages=menssages,
        total_menssages=total_menssages,
        menssages_complet=menssages_complet
    )

@dashboard_bp.route('/chart/excusas')
def chart_excusas():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total_excuses FROM pending_excuses")
    total_excuses = cursor.fetchone()["total_excuses"]

    cursor.execute("SELECT COUNT(*) AS total_accepted FROM accepted_excuses")
    total_accepted = cursor.fetchone()["total_accepted"]

    cursor.execute("SELECT COUNT(*) AS total_rejected FROM rejected_excuses")
    total_rejected = cursor.fetchone()["total_rejected"]

    cursor.close()

    return jsonify({
        "labels": ["Pendientes", "Aceptadas", "Rechazadas"],
        "data": [total_excuses, total_accepted, total_rejected]
    })

@dashboard_bp.route('/chart/usuarios')
def chart_usuarios():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total_user FROM users")
    total_user = cursor.fetchone()["total_user"]

    cursor.execute("SELECT COUNT(*) AS total_user FROM userunbailited")
    total_user_userunbailited = cursor.fetchone()["total_user"]

    cursor.execute("SELECT COUNT(*) AS total_user FROM students")
    total_students = cursor.fetchone()["total_user"]

    cursor.execute("SELECT rol, COUNT(*) AS total FROM users GROUP BY rol")
    roles_data = cursor.fetchall()

    total_admin = total_padre = total_profesor = total_administration = 0
    for row in roles_data:
        rol = row["rol"].lower()
        if rol == "admin":
            total_admin = row["total"]
        elif rol == "parent":
            total_padre = row["total"]
        elif rol == "teacher":
            total_profesor = row["total"]
        elif rol == "administration":
            total_administration = row["total"]

    cursor.close()

    return jsonify({
        "labels": [
            "Usuarios", 
            "Deshabilitados", 
            "Estudiantes", 
            "Admins", 
            "Padres", 
            "Profesores", 
            "Administración"
        ],
        "data": [
            total_user,
            total_user_userunbailited,
            total_students,
            total_admin,
            total_padre,
            total_profesor,
            total_administration
        ]
    })


@dashboard_bp.route('/solved', methods=['POST'])
def solved():
    message_id = request.form.get('message_id')
    
    if message_id:
        user_db = UserDatabase(mysql)
        user_db.delete_message(message_id)
        mensaje_texto = (
            f"Hola Usuario!\n"
            f"Nos complace informarle que su problema ha sido resuelto.\n"
        )
        send_whatsapp_message('+18498809890', mensaje_texto)

    return redirect(url_for('dashboard.dashboard'))

# Agregar usuario

@adduser_bp.route('/')
def show_form():
    return render_template('crud/adduser.html')

account_sid = "AC0c60b0f4c2b82eda97f8259d47423412"
auth_token  = "6e9ad64fa6d18f9d89a2321751aa47af"
twilio_whatsapp_number = 'whatsapp:+14155238886'

# Inicialización del cliente de Twilio
twilio_client = Client(account_sid, auth_token)


def send_whatsapp_message(to, message):
    """ Envía un mensaje de WhatsApp usando Twilio. """
    try:
        msg = twilio_client.messages.create(
            body=message,
            from_=twilio_whatsapp_number,
            to=f'whatsapp:{to}'
        )
        return msg.sid
    except Exception as e:
        print(f"❌ Error al enviar WhatsApp: {e}")
        raise

@adduser_bp.route('/get_students_by_grade/<grade>')
def get_students_by_grade(grade):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, name FROM students WHERE grade = %s", (grade,))
    students = cursor.fetchall()
    return jsonify(students)

@adduser_bp.route('/adduser', methods=['GET', 'POST'])
def add_user():
    user_db = UserDatabase(mysql)
    
    if request.method == 'GET':
        # Preparar datos para el formulario
        grades = user_db.get_grades()
        students = user_db.get_all_students()
        return render_template('crud/adduser.html',
                            grades=grades,
                            students=students)

    # Método POST
    try:
        # Datos básicos del usuario
        name = request.form.get('nameadd')
        rol = request.form.get('roladd')
        phone = request.form.get('phoneadd')
        idcard = request.form.get('idcard')
        password = request.form.get('passwordadd')
        
        # Validación básica
        if not all([name, rol, phone, idcard, password]):
            raise ValueError("Todos los campos son requeridos")

        # Insertar usuario principal
        user_db.insert_user(name, rol, phone, idcard, password, 'ASSETS/IMG/GenericImg/usuario.png')
        
        # Obtener ID del usuario recién creado
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID() as user_id")
        user_id = cursor.fetchone()['user_id']
        
        # Si es padre, procesar hijos
        if rol == 'parent':
            student_ids = request.form.getlist('student_id[]')
            
            # Validar que al menos haya un hijo
            if not student_ids or not all(student_ids):
                raise ValueError("Debe asignar al menos un hijo")
            
            # Asignar cada hijo al padre
            for student_id in student_ids:
                if student_id:  # Asegurarse que no esté vacío
                    user_db.assign_student_to_parent(user_id, student_id)
        
        mysql.connection.commit()
        return redirect(url_for('listcrud.listuser'))
    
    except Exception as e:
        mysql.connection.rollback()
        error_class = 'error'
        message = f'Error: {str(e)}'
        grades = user_db.get_grades()
        students = user_db.get_all_students()
        return render_template('crud/adduser.html', 
                            message=message, 
                            error_class=error_class,
                            grades=grades,
                            students=students)
    
@add_student_bp.route('/add_students', methods=['GET', 'POST'])
def add_student():
    
    if request.method == 'GET':
        user_db = UserDatabase(mysql)
        estudiantes = user_db.get_all_students()
        print('Estudiantes: ',estudiantes)
        grados = user_db.get_grades()
        return render_template('crud/add_students.html', estudiantes=estudiantes, grados=grados)

    if request.method == 'POST':
        try:
            name = request.form['studentName']
            grade = request.form['grado']

            if not all([name, grade]):
             return jsonify({"error": "Todos los campos son requeridos"}), 400

            user_db = UserDatabase(mysql)
            user_db.insert_students(name, grade)

            update = UpdateController(mysql)
            update.register('Agregaro', f'Se ha un nuevo estudiante {name} grado: {grade}')

         # Recargar estudiantes y grados después de agregar
            estudiantes = user_db.get_all_students()
            grados = user_db.get_grades()

            return url_for('shedule.save_schedule')

        except Exception as e:
            print({"error": str(e)})
            return jsonify({'error': 'Error al agregar el estudiante'}), 500


@add_student_bp.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    user_db = UserDatabase(mysql)
    
    if request.method == 'GET':
        # Obtener grados disponibles
        grados_disponibles = user_db.get_grades()  # Asumiendo que existe este método
        estudiantes = user_db.get_all_students()
        print(f'grados disponibles: {grados_disponibles}')
        return render_template('delete_student.html',
                            estudiantes=estudiantes,
                            grados_disponibles=grados_disponibles)
    
    elif request.method == 'POST':
        try:
            student_id = request.form['studentId']
            if not student_id:
                flash('Debe seleccionar un estudiante', 'error')
                return redirect(url_for('addstudents.delete_student'))
            
            user_db.delete_student(student_id)
            
            update = UpdateController(mysql)
            update.register('Eliminación', f'Estudiante eliminado: ID {student_id}')
            
            flash('Estudiante eliminado correctamente', 'success')
            return redirect(url_for('addstudents.delete_student'))
            
        except Exception as e:
            print(f'Error al eliminar estudiante: {str(e)}')
            flash('Error al eliminar el estudiante', 'error')
            return redirect(url_for('addstudents.delete_student'))
        

@add_grade_bp.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    
    if request.method == 'GET':
        return render_template('crud/add_students.html')  # Redirige al formulario

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            
            grade = request.form['grade']
            # Validar que los campos no estén vacíos
            if not all([ grade]):
                return jsonify({"error": "Todos los campos son requeridos"}), 400

            # Insertar en la base de datos
            user_db = UserDatabase(mysql)
            user_db.insert_grade( grade)
            
            update = UpdateController(mysql)
            update.register('Agregaro', f'Se ha un nuevo grado: {grade}')

            return render_template('crud/add_students.html')

        except Exception as e:
            print({"error": str(e)}), 500

@shedule_bp.route('/guardar_horario', methods=['GET', 'POST'])
def save_schedule():
    db = ScheduleDatabase(mysql)
    dbd = UserDatabase(mysql)
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        day = request.form['day_of_week']
        grade = request.form['grade']

        db.insert_schedule(teacher_id, day, grade)

        update = UpdateController(mysql)
        update.register('Asignado', f'Se ha asignado al profesor {teacher_id} el día: {day} para el grado: {grade}')
        
        return redirect(url_for('shedule.save_schedule'))  # Redirige después de guardar

    # Si es GET, obtener grados para mostrarlos en el formulario
    estudents = dbd.get_all_students()  # Este método debe devolver [{'id': ..., 'grade': ...}, ...]
    teachers = db.get_all_teachers()
    return render_template('crud/add_students.html', teachers=teachers, estudiantes=estudents)

@shedule_bp.route('/get_assigned_grades')
def get_assigned_grades():
    try:
        teacher_id = request.args.get('teacher_id')
        
        # Validación básica
        if not teacher_id or not teacher_id.isdigit():
            return jsonify({"error": "ID de profesor inválido"}), 400

        cursor = mysql.connection.cursor()
        
        try:
            # 1. Verificar que el profesor existe
            cursor.execute("SELECT id FROM users WHERE id = %s AND rol = 'teacher'", (teacher_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Profesor no encontrado"}), 404
            
            # 2. Obtener grados asignados con días formateados
            cursor.execute("""
                SELECT 
                    grade,
                    LOWER(TRIM(day_of_week)) as day_of_week
                FROM teacher_schedule
                WHERE teacher_id = %s
                ORDER BY 
                    CASE LOWER(TRIM(day_of_week))
                        WHEN 'lunes' THEN 1
                        WHEN 'martes' THEN 2
                        WHEN 'miércoles' THEN 3
                        WHEN 'jueves' THEN 4
                        WHEN 'viernes' THEN 5
                        ELSE 6
                    END
            """, (teacher_id,))
            
            results = cursor.fetchall()
            
            # Asegurar que todos los registros tengan datos válidos
            valid_results = []
            for row in results:
                if row['grade'] and row['day_of_week']:
                    valid_results.append({
                        'grade': row['grade'],
                        'day_of_week': row['day_of_week']
                    })
            
            return jsonify(valid_results)
            
        except Exception as db_error:
            print(f"Error en DB: {str(db_error)}")
            return jsonify({"error": "Error en la base de datos"}), 500
            
        finally:
            if cursor:
                cursor.close()
                
    except Exception as e:
        print(f"Error general: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@shedule_bp.route('/desasignar_grado', methods=['POST'])
def unassign_schedule():
    try:
        teacher_id = request.form.get('teacher_id')
        grade = request.form.get('grade')
        day_of_week = request.form.get('day_of_week')

        # Validación básica
        if not teacher_id or not teacher_id.isdigit() or not grade or not day_of_week:
            return jsonify({'error': 'Datos incompletos o inválidos'}), 400

        cursor = mysql.connection.cursor()
        
        # Eliminar el horario específico
        delete_query = """
            DELETE FROM teacher_schedule 
            WHERE teacher_id = %s AND grade = %s AND TRIM(LOWER(day_of_week)) = TRIM(LOWER(%s))
        """
        cursor.execute(delete_query, (teacher_id, grade, day_of_week))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'No se encontró coincidencia para eliminar'}), 404

        # Responder con una señal para que el frontend haga la redirección
        return jsonify({'success': True, 'redirect_url': url_for('addstudents.add_student')}), 200

    except Exception as e:
        print(f"Error al desasignar grado: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

    finally:
        if cursor:
            cursor.close()
    
# Editar usuario
@edit_user_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user_db = UserDatabase(mysql)
    
    if request.method == 'GET':
        usuario = user_db.get_users(table='users', condition=f"WHERE id = {user_id}")
        if not usuario:
            flash('Usuario no encontrado.', 'warning')
            return redirect(url_for('listcrud.listuser'))

        # Obtener hijos asignados si es padre
        children = []
        if usuario[0]['rol'] == 'parent':  # Acceso correcto para diccionarios
            children = user_db.get_students_by_parent(user_id)

        # Obtener todos los grados y estudiantes disponibles
        grades = user_db.get_grades()
        students = user_db.get_all_students()

        return render_template('crud/edit_user.html', 
                            usuario=usuario[0],
                            children=children,
                            grades=grades,
                            students=students)

    elif request.method == 'POST':
        name = request.form['nameedit']
        idcard = request.form['idcardedit']
        phone = request.form['phoneedit']
        rol = request.form['roledit']
        password = request.form['passwordedit']

        # Actualizar datos básicos del usuario
        user_db.update_user(user_id, name, rol, phone, idcard, password)

        # Si es padre, actualizar relaciones con hijos
        if rol == 'parent':
            # Eliminar relaciones existentes
            user_db.delete_parent_student_relations(user_id)
            
            # Agregar nuevas relaciones
            student_ids = request.form.getlist('student_id[]')
            for student_id in student_ids:
                if student_id:  # Asegurarse que no esté vacío
                    user_db.assign_student_to_parent(user_id, student_id)

        update = UpdateController(mysql)
        update.register('Editado', f'Se ha editado el usuario: {name}')
        flash(f'Usuario {user_id} actualizado con éxito.', 'success')
        return redirect(url_for('listcrud.listuser'))
    
# Deshabilitar usuario
@disable_user_bp.route('/disable_user/<int:user_id>', methods=['POST'])
def disable_user(user_id):
    try:
        user_db = UserDatabase(mysql)
        usuario = user_db.get_users(f"WHERE id = {user_id}")

        if not usuario:
            flash('Usuario no encontrado.', 'warning')
            return redirect(url_for('listcrud.listuser'))

        # Insertar el usuario en `userunbailited`
        usuario = usuario[0]
        cursor = user_db.get_cursor()
        cursor.execute(
            '''INSERT INTO userunbailited (id, name, rol, phone, idcard, last_updated) 
               VALUES (%s, %s, %s, %s, %s, %s)''', 
            (usuario['id'], usuario['name'], usuario['rol'], usuario['phone'], usuario['idcard'], usuario['last_updated'])
        )

        update = UpdateController(mysql)
        update.register('Deshabilitado', f'Se ha deshabilitado el ususario {usuario['name']}')
        # Eliminar el usuario de `users`
        user_db.delete_user(user_id)

        # Obtener solo los usuarios deshabilitados
        cursor.execute("SELECT * FROM userunbailited")
        disabled_users = cursor.fetchall()

        flash(f'Usuario {user_id} deshabilitado con éxito.', 'success')
        return render_template('crud/disable_user.html', disabled_users=disabled_users)

    except Exception as e:
        flash(f'Error al deshabilitar usuario: {e}', 'danger')

    return render_template('crud/disable_user.html')

# Eliminar usuario definitivamente
@disable_user_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        user_db = UserDatabase(mysql)
        user_db.delete_user(user_id, table='userunbailited')
        
        update = UpdateController(mysql)
        update.register('Eliminado', f'Se ha eliminado el ususario {user_id}')
        flash(f'Usuario {user_id} eliminado con éxito.', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {e}', 'danger')

    return redirect(url_for('listcrud.listuser'))

# Habilitar usuario
@enable_user_bp.route('/enable/<int:user_idenable>', methods=['POST'])
def enable_user(user_idenable):
    try:
        user_db = UserDatabase(mysql)
        
        # Obtener el usuario de 'userunbailited'
        usuario = user_db.get_users(f"WHERE id = {user_idenable}", table='userunbailited')
        
        if not usuario:
            flash('Usuario no encontrado.', 'warning')
            return redirect(url_for('listcrud.listuser'))

        # Insertar el usuario en la tabla 'users'
        usuario = usuario[0]
        cursor = user_db.get_cursor()
        cursor.execute(
            '''INSERT INTO users (name, rol, phone, idcard, password, last_updated) 
               VALUES (%s, %s, %s, %s, %s, %s)''', 
            (usuario['name'], usuario['rol'], usuario['phone'], usuario['idcard'], "123", usuario['last_updated'])
        )
        
        update = UpdateController(mysql)
        update.register('Habilitado', f'Se ha Habilitado el ususario {usuario['name']}')

        # Eliminar el usuario de 'userunbailited'
        user_db.delete_user(user_idenable, table='userunbailited')

        flash(f'Usuario {user_idenable} habilitado con éxito.', 'success')
    except Exception as e:
        print(f'Error al habilitar usuario: {e}', 'danger')

    return redirect(url_for('listcrud.listuser'))

# Visualizar lista de usuarios
@listcrud_bp.route('', methods=['GET'])
def listuser():
    # 1️⃣ Parámetros de paginación
    page     = request.args.get('page',   1,   type=int)
    per_page = request.args.get('per_page', 7, type=int)
    offset   = (page - 1) * per_page

    # 2️⃣ Parámetro de búsqueda
    search = request.args.get('search', '', type=str).strip()
    
    # 3️⃣ Construimos la condición SQL y los params
    condition = "WHERE rol = 'parent'"
    params    = []
    if search:
        # Buscamos en name, idcard y phone (ajusta columnas según tu esquema)
        condition += " AND (name LIKE %s OR idcard LIKE %s OR phone LIKE %s)"
        term = f"%{search}%"
        params = [term, term, term]

    # 4️⃣ Acceso a datos
    user_db     = UserDatabase(mysql)
    total_users = user_db.count_users(condition=condition, params=params)
    usuarios    = user_db.get_users(condition=condition, params=params, limit=per_page, offset=offset)

    # 5️⃣ Paginación
    total_pages = math.ceil(total_users / per_page)
    has_prev    = page > 1
    has_next    = page < total_pages

    # 6️⃣ Render
    return render_template(
        'crud/listuser.html',
        usuarios=usuarios,
        page=page,
        per_page=per_page,
        total_users=total_users,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        search=search
    )

#visualiza lista de estudiantes

@listcrud_bp.route('/listuser', methods=['GET'])
def liststudent():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    offset = (page - 1) * per_page

    search = request.args.get('search', '', type=str).strip()
    selected_grade = request.args.get('grade', '', type=str).strip()
    
    # Construcción de condición y parámetros
    condition = "WHERE 1=1"
    params = []

    if search:
        condition += " AND (name LIKE %s OR id LIKE %s)"
        term = f"%{search}%"
        params.extend([term, term])

    if selected_grade:
        condition += " AND grade = %s"
        params.append(selected_grade)

    # Acceso a datos
    user_db = UserDatabase(mysql)
    
    # Obtener todos los grados disponibles para el filtro
    available_grades = user_db.get_available_grades()
    
    total_students = user_db.count_students(condition=condition, params=params)
    students = user_db.get_students(condition=condition, params=params, limit=per_page, offset=offset)

    total_pages = math.ceil(total_students / per_page)
    has_prev = page > 1
    has_next = page < total_pages

    return render_template(
        'crud/students_list.html',
        students=students,
        page=page,
        per_page=per_page,
        total_students=total_students,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        search=search,
        available_grades=available_grades,
        selected_grade=selected_grade
    )

# Visualizar lista de trabajadores
@listworker_bp.route('/listworker', methods=['GET'])
def listworker():
    # Parámetros de paginación
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 7, type=int)
    offset   = (page - 1) * per_page

    # Parámetro de búsqueda
    search = request.args.get('search', '', type=str).strip()

    # Condición y parámetros
    condition = "WHERE rol != 'parent'"  # Solo trabajadores (no padres)
    params = []

    if search:
        condition += " AND (name LIKE %s OR idcard LIKE %s OR phone LIKE %s)"
        term = f"%{search}%"
        params = [term, term, term]

    # Acceso a base de datos
    user_db = UserDatabase(mysql)
    total_users = user_db.count_users(condition=condition, params=params)
    usuarios = user_db.get_users(
        condition=condition,
        params=params,
        limit=per_page,
        offset=offset
    )

    # Cálculo de paginación
    total_pages = max(math.ceil(total_users / per_page), 1)
    has_prev = page > 1
    has_next = page < total_pages

    return render_template(
        'crud/listworkers.html',
        usuarios=usuarios,
        page=page,
        per_page=per_page,
        total_users=total_users,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        search=search
    )


# Visualizar lista de usuarios deshabilitados
@disable_bp.route('/disable')
def disable():
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 7, type=int)
    offset   = (page - 1) * per_page
    search   = request.args.get('search', '', type=str).strip()

    condition = None
    params = []
    
    user_db = UserDatabase(mysql)

    total_disabled = user_db.count_users(condition=condition, params=params, table='userunbailited')
    total_pages = max(math.ceil(total_disabled / per_page), 1)
    has_prev = page > 1
    has_next = page < total_pages

    usuarios = user_db.get_disabled_users(per_page=per_page, offset=offset)

    return render_template(
        'crud/disable_user.html',
        usuarios=usuarios,
        page=page,
        per_page=per_page,
        total_disabled=total_disabled,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        search=search
    )


@ver_usuario_bp.route('/get_user_profile/<int:user_id>')
def get_user_profile(user_id):
    db = UserDatabase(mysql)
    try:
        # Obtener información del usuario
        user_data = db.get_users(f"WHERE id = {user_id}")
        
        if not user_data:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        user_data = user_data[0]
        
        # Formatear los datos para la respuesta (sin excusas)
        user_profile = {
            'nombre': user_data['name'],
            'rol': user_data['rol'],
            'id': user_data['id'],
            'cedula': user_data['idcard'],
            'telefono': user_data['phone'],
            'ultima_actividad': user_data['last_updated'].strftime('%d/%m/%Y %H:%M'),
            'estado': 'Activo'
        }
        
        return jsonify(user_profile)
    except Exception as e:
        print(f"Error al obtener perfil de usuario: {e}")
        return jsonify({'error': str(e)}), 500


reportes = Blueprint("reportes", __name__)

class UserRepository:
    def __init__(self, mysql):
        self.mysql = mysql
        
    def get_cursor(self):
        try:
            return self.mysql.connection.cursor()  # Configurado para devolver diccionarios
        except Exception as e:
            print(f"Error al obtener el cursor: {e}")
            return None
    
    def get_users(self, condition='', params=None, table='users', limit=None, offset=None):
        cursor = None
        try:
            cursor = self.get_cursor()
            if not cursor:
                return []

            sql = f"""
                SELECT 
                    id, 
                    name,
                    rol,
                    idcard,
                    phone,
                    last_updated as last_update
                FROM `{table}` {condition}
            """
            all_params = params.copy() if params else []

            if limit is not None and offset is not None:
                sql += " LIMIT %s OFFSET %s"
                all_params += [limit, offset]

            cursor.execute(sql, all_params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
                
class ReporteTodosUsuarios:
    def __init__(self, user_repository):
        self.BASE_DIR = Path(__file__).parent.absolute()
        self.OUTPUT_DIR = self.BASE_DIR / "reportes" / "archivos"
        self.LOGO_PATH = Path(r"C:\Users\DUNDO\Desktop\proyectos\GESDE\src\static\ASSETS\IMG\GenericImg\GedesLogo.png")
        
        if not self.LOGO_PATH.exists():
            raise FileNotFoundError(f"Logo no encontrado en: {self.LOGO_PATH}")
        
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.user_repo = user_repository
        
        # Estilos mejorados con paleta profesional
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='TitleGESDE',
            parent=self.styles['Title'],
            fontSize=18,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1565C0"),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='SubtitleGESDE',
            parent=self.styles['Heading2'],
            fontSize=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#0D47A1"),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='ResumenTitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1976D2"),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='ResumenText',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            leftIndent=20,
            textColor=colors.HexColor("#424242")
        ))
        self.styles.add(ParagraphStyle(
            name='HeaderText',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#616161"),
            fontName='Helvetica-Oblique'
        ))

    def _safe_strftime(self, date_obj):
        if not date_obj:
            return "N/A"
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(date_obj, str):
            try:
                return datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return date_obj
        return str(date_obj)

    def _create_pie_chart(self, data, width=200, height=150):
        """Crea un gráfico circular profesional con leyenda"""
        drawing = Drawing(width, height)
        
        # Paleta de colores profesional
        colors_pie = [
            colors.HexColor("#1565C0"),  # Azul oscuro
            colors.HexColor("#42A5F5"),  # Azul medio
            colors.HexColor("#90CAF9"),  # Azul claro
            colors.HexColor("#BBDEFB"),  # Azul muy claro
            colors.HexColor("#0D47A1")   # Azul oscuro alternativo
        ]
        
        pie = Pie()
        pie.x = 20
        pie.y = 20
        pie.width = width - 40
        pie.height = height - 40
        pie.data = [d[1] for d in data]
        pie.labels = [d[0] for d in data]
        pie.sideLabels = True
        pie.simpleLabels = False
        pie.slices.strokeWidth = 0.5
        pie.slices.fontSize = 8
        pie.slices.labelRadius = 0.75
        pie.slices.popout = 5
        
        # Aplicar estilos a los segmentos
        for i, color in enumerate(colors_pie):
            if i < len(pie.slices):
                pie.slices[i].fillColor = color
                pie.slices[i].strokeColor = colors.white
                pie.slices[i].strokeWidth = 0.5
                if i == 0:
                    pie.slices[i].popout = 10
        
        # Leyenda profesional
        legend = Legend()
        legend.x = width - 100
        legend.y = height - 20
        legend.colorNamePairs = [(colors_pie[i], f"{data[i][0]} ({data[i][1]})") for i in range(len(data))]
        legend.fontName = 'Helvetica'
        legend.fontSize = 7
        legend.columnMaximum = 1
        legend.boxAnchor = 'ne'
        legend.dx = 5
        legend.dy = 5
        legend.deltax = 5
        legend.deltay = 5
        legend.autoXPadding = 5
        
        drawing.add(pie)
        drawing.add(legend)
        return drawing

    def _create_bar_chart(self, data, width=200, height=150):
        """Crea un gráfico de barras vertical profesional"""
        drawing = Drawing(width, height)
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 30
        bc.width = width - 60
        bc.height = height - 50
        bc.data = [[d[1] for d in data]]
        bc.bars.fillColor = colors.HexColor("#42A5F5")
        bc.bars.strokeColor = colors.white
        bc.bars.strokeWidth = 0.5
        
        # Configuración de ejes
        bc.categoryAxis.categoryNames = [d[0] for d in data]
        bc.categoryAxis.labels.fontName = 'Helvetica'
        bc.categoryAxis.labels.fontSize = 7
        bc.categoryAxis.labels.angle = 45
        bc.categoryAxis.labels.dy = -10
        bc.valueAxis.labels.fontName = 'Helvetica'
        bc.valueAxis.labels.fontSize = 7
        
        # Efectos visuales
        bc.barSpacing = 2
        bc.groupSpacing = 10
        bc.valueAxis.avoidBoundSpace = 5
        
        # Líneas de guía
        bc.valueAxis.gridStrokeColor = colors.HexColor("#E0E0E0")
        bc.valueAxis.gridStrokeWidth = 0.5
        
        drawing.add(bc)
        return drawing

    def generar_pdf(self, generado_por, lista=None, titulo_especial=None, mostrar_graficos=True, table='users'):
        # Configuración del documento
        # Si se especifica un título especial, úsalo en el nombre del archivo
        
        if lista is None:
            # Usar el parámetro table para obtener los usuarios
            usuarios = self.user_repo.get_users(table=table)
        else:
            usuarios = lista
        nombre_archivo_base = "reporte_usuarios_mejorado"
        if titulo_especial:
            nombre_archivo_base = f"reporte_{titulo_especial.lower().replace(' ', '_')}"
            
        nombre_archivo = self.OUTPUT_DIR / f"{nombre_archivo_base}.pdf"
        doc = SimpleDocTemplate(str(nombre_archivo), pagesize=letter, 
                              leftMargin=40, rightMargin=40,
                              topMargin=60, bottomMargin=60)
        elementos = []

        # --- ENCABEZADO MEJORADO ---
        # Si hay un título especial, úsalo en el encabezado
        titulo_reporte = "REPORTE COMPLETO DE USUARIOS"
        if titulo_especial:
            titulo_reporte = titulo_especial
            
        header_table = Table([
            [Image(self.LOGO_PATH, width=140, height=70), 
             Paragraph("<font color='#1565C0'><b>GESDE</b></font> - Gestión de Excusas Online<br/>"
                      f"<font size=14 color='#0D47A1'>{titulo_reporte}</font>", 
                      self.styles['TitleGESDE'])]
        ], colWidths=[160, 340])
        
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#E3F2FD"))
        ]))
        
        elementos.append(header_table)
        
        # Información de generación
        elementos.extend([
            Paragraph(f"<font color='#616161'>Generado por:</font> <b>{generado_por or 'Sistema'}</b>", 
                     self.styles['HeaderText']),
            Paragraph(f"<font color='#616161'>Fecha de generación:</font> <b>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</b>", 
                     self.styles['HeaderText']),
            Spacer(1, 25)
        ])

        # --- RESUMEN EJECUTIVO AL INICIO (para reportes especiales) ---
        if titulo_especial and "PADRES" in titulo_especial.upper():
            elementos.extend([
                Paragraph("Resumen Ejecutivo", self.styles['SubtitleGESDE']),
                Spacer(1, 10)
            ])
            
            # IMPORTANTE: Usar la lista proporcionada o recuperar todos los usuarios si no se proporciona
            if lista is None:
                usuarios = self.user_repo.get_users(table='users')
            else:
                usuarios = lista
                
            total_padres = len(usuarios)
            
            # Extraer estadísticas específicas para padres
            tiene_telefono = sum(1 for user in usuarios if user.get('phone') and user.get('phone') != 'N/A' and user.get('phone') != '')
            porcentaje_telefonos = (tiene_telefono / total_padres * 100) if total_padres > 0 else 0
            
            # Verificar si hay datos de última actualización
            fechas_actualizacion = []
            for user in usuarios:
                fecha_str = user.get('last_update')
                if fecha_str:
                    try:
                        fecha = datetime.strptime(str(fecha_str), '%Y-%m-%d %H:%M:%S')
                        fechas_actualizacion.append(fecha)
                    except (ValueError, TypeError):
                        pass
            
            # Encontrar la fecha más reciente y más antigua de actualización
            fecha_mas_reciente = max(fechas_actualizacion) if fechas_actualizacion else None
            fecha_mas_antigua = min(fechas_actualizacion) if fechas_actualizacion else None
            
            # Tabla de resumen
            resumen_data = [
                ["Total de padres registrados:", f"{total_padres}"],
                ["Padres con teléfono registrado:", f"{tiene_telefono} ({porcentaje_telefonos:.1f}%)"],
            ]
            
            if fecha_mas_reciente:
                resumen_data.append(["Registro más reciente:", f"{fecha_mas_reciente.strftime('%d/%m/%Y %H:%M:%S')}"])
            if fecha_mas_antigua:
                resumen_data.append(["Registro más antiguo:", f"{fecha_mas_antigua.strftime('%d/%m/%Y %H:%M:%S')}"])
                
            tabla_resumen = Table(resumen_data, colWidths=[200, 250])
            tabla_resumen.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#212121")),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0"))
            ]))
            
            elementos.append(tabla_resumen)
            elementos.append(Spacer(1, 15))
            
        # --- TABLA DE USUARIOS ---
        # IMPORTANTE: Usar la lista proporcionada o recuperar todos los usuarios si no se proporciona
        if lista is None:
            usuarios = self.user_repo.get_users(table='users')
        else:
            usuarios = lista
        
        # Preparar tabla
        encabezados = ["ID", "NOMBRE", "ROL", "CÉDULA", "TELÉFONO", "ÚLTIMA ACTUALIZACIÓN"]
        data = [encabezados]
        
        for user in usuarios:
            row = [
                str(user.get('id', 'N/A')),
                str(user.get('name', 'N/A')),
                str(user.get('rol', 'N/A')),
                str(user.get('idcard', 'N/A')),
                str(user.get('phone', 'N/A')),
                self._safe_strftime(user.get('last_update', 'N/A'))
            ]
            data.append(row)
        
        tabla = Table(data, colWidths=[40, 120, 80, 90, 80, 110], repeatRows=1)
        
        estilo_tabla = TableStyle([
            # Cabecera
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Cuerpo
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#212121")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ])
        
        tabla.setStyle(estilo_tabla)
        elementos.append(tabla)
        
        # --- SECCIÓN DE GRÁFICOS ---
        # Solo mostrar gráficos si mostrar_graficos es True
        if mostrar_graficos:
            elementos.extend([
                PageBreak(),
                Spacer(1, 20),
                Paragraph("Análisis Estadístico de Usuarios", self.styles['ResumenTitle']),
                Spacer(1, 15)
            ])
            
            # Estadísticas
            total_usuarios = len(usuarios)
            
            # Para el caso específico de padres, crear análisis más detallados
            if titulo_especial and "PADRES" in titulo_especial.upper():
                
                # Análisis por fechas de actualización (para ver cuándo se registraron/actualizaron)
                fechas_actualizacion = {}
                for user in usuarios:
                    fecha_str = user.get('last_update')
                    if fecha_str:
                        try:
                            fecha = datetime.strptime(str(fecha_str), '%Y-%m-%d %H:%M:%S')
                            mes_año = fecha.strftime('%b %Y')  # Formato "Mes Año"
                            fechas_actualizacion[mes_año] = fechas_actualizacion.get(mes_año, 0) + 1
                        except (ValueError, TypeError):
                            pass
                
                # Ordenar por fecha (del más antiguo al más reciente)
                fechas_sorted = sorted(fechas_actualizacion.items(), 
                                      key=lambda x: datetime.strptime(x[0], '%b %Y'))
                
                # Crear gráfico de barras de registro/actualización por mes
                if fechas_sorted:
                    bar_chart_fechas = self._create_bar_chart(fechas_sorted, width=400, height=200)
                    
                    # Tabla para organizar el gráfico
                    chart_table = Table([
                        ["Registro/Actualización de Padres por Mes"],
                        [bar_chart_fechas],
                        [Paragraph("Este gráfico muestra la distribución de registros/actualizaciones a lo largo del tiempo", 
                                  self.styles['ResumenText'])]
                    ], colWidths=[500], rowHeights=[20, 200, 30])
                    
                    chart_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
                        ('FONTSIZE', (0, 2), (-1, 2), 9)
                    ]))
                    
                    elementos.append(chart_table)
                    elementos.append(Spacer(1, 20))
                
                # Análisis de padres con/sin teléfono
                telefonos = {
                    "Con teléfono": sum(1 for user in usuarios if user.get('phone') and user.get('phone') != 'N/A' and user.get('phone') != ''),
                    "Sin teléfono": sum(1 for user in usuarios if not user.get('phone') or user.get('phone') == 'N/A' or user.get('phone') == '')
                }
                
                telefonos_data = [(k, v) for k, v in telefonos.items() if v > 0]
                
                if telefonos_data:
                    pie_telefonos = self._create_pie_chart(telefonos_data, width=300, height=200)
                    
                    chart_table = Table([
                        ["Distribución de Padres con/sin Teléfono Registrado"],
                        [pie_telefonos],
                        [Paragraph("Este gráfico muestra la proporción de padres que tienen un número de teléfono registrado",
                                  self.styles['ResumenText'])]
                    ], colWidths=[500], rowHeights=[20, 200, 30])
                    
                    chart_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
                        ('FONTSIZE', (0, 2), (-1, 2), 9)
                    ]))
                    
                    elementos.append(chart_table)
                    
            else:  # Para reportes que no son específicos de padres
                # Estadísticas generales por rol
                roles = {}
                for user in usuarios:
                    rol = user.get('rol', 'No definido')
                    roles[rol] = roles.get(rol, 0) + 1
                
                roles_sorted = sorted(roles.items(), key=lambda x: x[1], reverse=True)
                
                # Gráficos uno al lado del otro
                if roles_sorted:  # Verificar que hay datos para los gráficos
                    pie_chart = self._create_pie_chart(roles_sorted, width=250, height=180)
                    bar_chart = self._create_bar_chart(roles_sorted, width=250, height=180)
                    
                    # Tabla para organizar los gráficos
                    charts_table = Table([
                        ["Distribución por Roles", "Cantidad por Rol"],
                        [pie_chart, bar_chart],
                        [Paragraph(f"<b>Total usuarios:</b> {total_usuarios}", self.styles['ResumenText']),
                         Paragraph("Análisis de distribución de roles", self.styles['ResumenText'])]
                    ], colWidths=[doc.width/2.0]*2, rowHeights=[20, 180, 30])
                    
                    charts_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
                        ('FONTSIZE', (0, 2), (-1, 2), 9)
                    ]))
                    
                    elementos.append(charts_table)
            
            # --- RESUMEN FINAL ---
            elementos.extend([
                PageBreak(),
                Spacer(1, 15),
                Paragraph("Resumen Final", self.styles['SubtitleGESDE']),
                Spacer(1, 10)
            ])
            
            # Detalles estadísticos
            ultima_actualizacion = None
            for user in usuarios:
                fecha_str = user.get('last_update')
                if fecha_str:
                    try:
                        fecha = datetime.strptime(str(fecha_str), '%Y-%m-%d %H:%M:%S')
                        if ultima_actualizacion is None or fecha > ultima_actualizacion:
                            ultima_actualizacion = fecha
                    except (ValueError, TypeError):
                        pass
            
            # Para el caso específico de padres, mostrar un resumen enfocado en ese rol
            if titulo_especial and "PADRES" in titulo_especial.upper():
                resumen_content = [
                    Paragraph("<b>Información del Registro de Padres:</b>", self.styles['ResumenText']),
                    Spacer(1, 5)
                ]
                
                # Analizar completitud de datos
                datos_completos = sum(1 for user in usuarios 
                                    if (user.get('phone') and user.get('phone') != 'N/A' and user.get('phone') != '') and
                                       (user.get('idcard') and user.get('idcard') != 'N/A' and user.get('idcard') != ''))
                
                porcentaje_completo = (datos_completos / total_usuarios) * 100 if total_usuarios > 0 else 0
                
                resumen_content.extend([
                    Paragraph(f"• Total de padres registrados: <b>{total_usuarios}</b>", self.styles['ResumenText']),
                    Paragraph(f"• Padres con datos completos (teléfono e identificación): <b>{datos_completos}</b> ({porcentaje_completo:.1f}%)", 
                             self.styles['ResumenText']),
                    Spacer(1, 5)
                ])
                
                # Análisis de último registro
                if ultima_actualizacion:
                    # Calcular días desde la última actualización
                    dias_desde_actualizacion = (datetime.now() - ultima_actualizacion).days
                    resumen_content.extend([
                        Paragraph(f"• Última actualización de datos: <b>{ultima_actualizacion.strftime('%d/%m/%Y')}</b> ({dias_desde_actualizacion} días atrás)", 
                                 self.styles['ResumenText']),
                        Spacer(1, 5)
                    ])
                    
                # Recomendaciones basadas en el análisis
                resumen_content.extend([
                    Spacer(1, 10),
                    Paragraph("<b>Recomendaciones:</b>", self.styles['ResumenText']),
                    Spacer(1, 5)
                ])
                
                if porcentaje_completo < 90:
                    resumen_content.append(
                        Paragraph("• Se recomienda completar la información de contacto de los padres para mejorar la comunicación.", 
                                 self.styles['ResumenText'])
                    )
                
                if ultima_actualizacion and dias_desde_actualizacion > 90:
                    resumen_content.append(
                        Paragraph("• Es recomendable actualizar la información de los padres, ya que han pasado más de 90 días desde la última actualización.", 
                                 self.styles['ResumenText'])
                    )
                
                elementos.extend(resumen_content)
                
            else:  # Para reportes que no son específicos de padres
                resumen_content = [
                    Paragraph(f"<b>Total de usuarios registrados:</b> {total_usuarios}", self.styles['ResumenText']),
                    Spacer(1, 5),
                    Paragraph("<b>Distribución por roles:</b>", self.styles['ResumenText'])
                ]
                
                roles_sorted = sorted(roles.items(), key=lambda x: x[1], reverse=True)
                for rol, cantidad in roles_sorted:
                    porcentaje = (cantidad / total_usuarios) * 100 if total_usuarios > 0 else 0
                    resumen_content.extend([
                        Paragraph(f"• {rol}: {cantidad} usuarios ({porcentaje:.1f}%)", 
                                 self.styles['ResumenText']),
                        Spacer(1, 3)
                    ])
                
                if ultima_actualizacion:
                    resumen_content.extend([
                        Spacer(1, 10),
                        Paragraph(f"<b>Última actualización en el sistema:</b> {ultima_actualizacion.strftime('%d/%m/%Y %H:%M:%S')}", 
                                 self.styles['ResumenText'])
                    ])
                
                elementos.extend(resumen_content)
                Paragraph("Análisis Estadístico de Usuarios", self.styles['ResumenTitle']),
                Spacer(1, 15)
           
            
            # Estadísticas
            total_usuarios = len(usuarios)
            roles = {}
            for user in usuarios:
                rol = user.get('rol', 'No definido')
                roles[rol] = roles.get(rol, 0) + 1
            
            roles_sorted = sorted(roles.items(), key=lambda x: x[1], reverse=True)
            
            # Gráficos uno al lado del otro
            if roles_sorted:  # Verificar que hay datos para los gráficos
                pie_chart = self._create_pie_chart(roles_sorted, width=250, height=180)
                bar_chart = self._create_bar_chart(roles_sorted, width=250, height=180)
                
                # Tabla para organizar los gráficos
                charts_table = Table([
                    ["Distribución por Roles", "Cantidad por Rol"],
                    [pie_chart, bar_chart],
                    [Paragraph(f"<b>Total usuarios:</b> {total_usuarios}", self.styles['ResumenText']),
                     Paragraph("Análisis de distribución de roles", self.styles['ResumenText'])]
                ], colWidths=[doc.width/2.0]*2, rowHeights=[20, 180, 30])
                
                charts_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                    ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
                    ('FONTSIZE', (0, 2), (-1, 2), 9)
                ]))
                
                elementos.append(charts_table)
                
                # --- RESUMEN FINAL ---
                elementos.extend([
                    Spacer(1, 25),
                    Paragraph("Resumen Ejecutivo", self.styles['ResumenTitle']),
                    Spacer(1, 10)
                ])
                
                # Detalles estadísticos
                ultima_actualizacion = None
                for user in usuarios:
                    fecha_str = user.get('last_update')
                    if fecha_str:
                        try:
                            fecha = datetime.strptime(str(fecha_str), '%Y-%m-%d %H:%M:%S')
                            if ultima_actualizacion is None or fecha > ultima_actualizacion:
                                ultima_actualizacion = fecha
                        except (ValueError, TypeError):
                            pass
                
                resumen_content = [
                    Paragraph(f"<b>Total de usuarios registrados:</b> {total_usuarios}", self.styles['ResumenText']),
                    Spacer(1, 5),
                    Paragraph("<b>Distribución por roles:</b>", self.styles['ResumenText'])
                ]
                
                for rol, cantidad in roles_sorted:
                    porcentaje = (cantidad / total_usuarios) * 100 if total_usuarios > 0 else 0
                    resumen_content.extend([
                        Paragraph(f"• {rol}: {cantidad} usuarios ({porcentaje:.1f}%)", 
                                 self.styles['ResumenText']),
                        Spacer(1, 3)
                    ])
                
                if ultima_actualizacion:
                    resumen_content.extend([
                        Spacer(1, 10),
                        Paragraph(f"<b>Última actualización en el sistema:</b> {ultima_actualizacion.strftime('%d/%m/%Y %H:%M:%S')}", 
                                 self.styles['ResumenText'])
                    ])
                
                elementos.extend(resumen_content)
        
        # --- PIE DE PÁGINA ---
        elementos.append(PageBreak())
        elementos.extend([
            Spacer(1, 20),
            Paragraph("Información del Reporte", self.styles['ResumenTitle']),
            Spacer(1, 10),
            Paragraph("Este documento fue generado automáticamente por el sistema GESDE", self.styles['ResumenText']),
            Paragraph("Los datos reflejan el estado actual al momento de generación", self.styles['ResumenText']),
            Spacer(1, 5),
            Paragraph(f"Documento generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}", 
                     self.styles['HeaderText']),
            Spacer(1, 10),
            Paragraph("GESDE - Gestión de Excusas Online", 
                     ParagraphStyle(name='Footer', fontSize=10, textColor=colors.HexColor("#757575")))
        ])
        
        # Generar PDF
        doc.build(elementos)
        return str(nombre_archivo)


class ExcusasRepository:
    def __init__(self, mysql):
        self.mysql = mysql
        
    def get_cursor(self):
        try:
            return self.mysql.connection.cursor()  # Configurado para devolver diccionarios
        except Exception as e:
            print(f"Error al obtener el cursor: {e}")
            return None
    
    def get_excusas(self, condition='', params=None, table='pending_excuses', limit=None, offset=None):
        cursor = None
        try:
            cursor = self.get_cursor()
            if not cursor:
                return []

            sql = f"""
                SELECT 
                    id_excuse, 
                    parent_name,
                    student_name,
                    grade,
                    reason,
                    id_user,
                    excuse_date,
                    excuse_duration,
                    specification,
                    state
                FROM `{table}` {condition}
            """
            all_params = params.copy() if params else []

            if limit is not None and offset is not None:
                sql += " LIMIT %s OFFSET %s"
                all_params += [limit, offset]

            cursor.execute(sql, all_params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener excusas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

class ReporteExcusasPendientes:
    def __init__(self, excusas_repository):
        self.BASE_DIR = Path(__file__).parent.absolute()
        self.OUTPUT_DIR = self.BASE_DIR / "reportes" / "archivos"
        self.LOGO_PATH = Path(r"C:\Users\DUNDO\Desktop\proyectos\GESDE\src\static\ASSETS\IMG\GenericImg\GedesLogo.png")
        
        if not self.LOGO_PATH.exists():
            raise FileNotFoundError(f"Logo no encontrado en: {self.LOGO_PATH}")
        
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.excusas_repo = excusas_repository
        
        # Estilos mejorados
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Configura los estilos personalizados para el reporte"""
        self.styles.add(ParagraphStyle(
            name='TitleGESDE',
            parent=self.styles['Title'],
            fontSize=18,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1565C0"),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='SubtitleGESDE',
            parent=self.styles['Heading2'],
            fontSize=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#0D47A1"),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='ResumenTitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1976D2"),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='ResumenText',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            leftIndent=20,
            textColor=colors.HexColor("#424242")
        ))
        self.styles.add(ParagraphStyle(
            name='HeaderText',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#616161"),
            fontName='Helvetica-Oblique'
        ))

    def _safe_strftime(self, date_obj):
        """Formatea fechas de manera segura"""
        if not date_obj:
            return "N/A"
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(date_obj, str):
            try:
                return datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return date_obj
        return str(date_obj)

    def _create_pie_chart(self, data, width=200, height=150):
        """Crea un gráfico circular profesional con leyenda"""
        drawing = Drawing(width, height)
        colors_pie = [
            colors.HexColor("#1565C0"), colors.HexColor("#42A5F5"),
            colors.HexColor("#90CAF9"), colors.HexColor("#BBDEFB"),
            colors.HexColor("#0D47A1")
        ]
        
        pie = Pie()
        pie.x = 20
        pie.y = 20
        pie.width = width - 40
        pie.height = height - 40
        pie.data = [d[1] for d in data]
        pie.labels = [d[0] for d in data]
        pie.sideLabels = True
        pie.simpleLabels = False
        pie.slices.strokeWidth = 0.5
        pie.slices.fontSize = 8
        pie.slices.labelRadius = 0.75
        pie.slices.popout = 5
        
        for i, color in enumerate(colors_pie):
            if i < len(pie.slices):
                pie.slices[i].fillColor = color
                pie.slices[i].strokeColor = colors.white
                pie.slices[i].strokeWidth = 0.5
                if i == 0:
                    pie.slices[i].popout = 10
        
        legend = Legend()
        legend.x = width - 100
        legend.y = height - 20
        legend.colorNamePairs = [(colors_pie[i], f"{data[i][0]} ({data[i][1]})") for i in range(len(data))]
        legend.fontName = 'Helvetica'
        legend.fontSize = 7
        legend.columnMaximum = 1
        legend.boxAnchor = 'ne'
        
        drawing.add(pie)
        drawing.add(legend)
        return drawing

    def _create_bar_chart(self, data, width=400, height=200):
        """Crea un gráfico de barras vertical profesional"""
        drawing = Drawing(width, height)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 30
        bc.width = width - 60
        bc.height = height - 50
        bc.data = [[d[1] for d in data]]
        bc.bars.fillColor = colors.HexColor("#42A5F5")
        bc.bars.strokeColor = colors.white
        bc.bars.strokeWidth = 0.5
        
        bc.categoryAxis.categoryNames = [d[0] for d in data]
        bc.categoryAxis.labels.fontName = 'Helvetica'
        bc.categoryAxis.labels.fontSize = 7
        bc.categoryAxis.labels.angle = 45
        bc.categoryAxis.labels.dy = -10
        bc.valueAxis.labels.fontName = 'Helvetica'
        bc.valueAxis.labels.fontSize = 7
        
        bc.barSpacing = 2
        bc.groupSpacing = 10
        bc.valueAxis.gridStrokeColor = colors.HexColor("#E0E0E0")
        
        drawing.add(bc)
        return drawing

    def _generate_header(self, titulo_reporte):
        """Genera el encabezado del reporte"""
        header_table = Table([
            [Image(self.LOGO_PATH, width=140, height=70), 
             Paragraph(f"<font color='#1565C0'><b>GESDE</b></font> - Gestión de Excusas Online<br/>"
                      f"<font size=14 color='#0D47A1'>{titulo_reporte}</font>", 
                      self.styles['TitleGESDE'])]
        ], colWidths=[160, 340])
        
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#E3F2FD"))
        ]))
        return header_table

    def _calculate_statistics(self, excusas):
        """Calcula todas las estadísticas necesarias para el reporte"""
        estados = {}
        razones = {}
        grados = {}
        fechas_excusas = []
        
        for exc in excusas:
            # Estadísticas por estado
            estado = exc.get('state', 'No definido')
            estados[estado] = estados.get(estado, 0) + 1
            
            # Estadísticas por razón
            razon = exc.get('reason', 'No especificada')
            razones[razon] = razones.get(razon, 0) + 1
            
            # Estadísticas por grado
            grado = exc.get('grade', 'No especificado')
            grados[grado] = grados.get(grado, 0) + 1
            
            # Manejo de fechas
            fecha_str = exc.get('excuse_date')
            if fecha_str:
                try:
                    fecha = datetime.strptime(str(fecha_str), '%Y-%m-%d %H:%M:%S')
                    fechas_excusas.append(fecha)
                except (ValueError, TypeError):
                    pass
        
        # Procesamiento adicional
        fecha_mas_reciente = max(fechas_excusas) if fechas_excusas else None
        fecha_mas_antigua = min(fechas_excusas) if fechas_excusas else None
        top_razones = sorted(razones.items(), key=lambda x: x[1], reverse=True)[:3]
        top_motivos = sorted(razones.items(), key=lambda x: x[1], reverse=True)[:5]
        grados_data = sorted(grados.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'estados': estados,
            'razones': razones,
            'grados': grados_data,
            'fecha_mas_reciente': fecha_mas_reciente,
            'fecha_mas_antigua': fecha_mas_antigua,
            'top_razones': top_razones,
            'top_motivos': top_motivos,
            'total_excusas': len(excusas)
        }

    def generar_pdf(self, generado_por, lista=None, titulo_especial=None, mostrar_graficos=True, tabla='pending_excuses'):
        datos = self.excusas_repo.get_excusas(table=tabla)
    
        if not datos:
            raise ValueError(f"No hay datos en la tabla {tabla} para generar el PDF.")
        """Genera el reporte PDF completo"""
        # Configuración inicial
        nombre_archivo_base = "reporte_excusas_pendientes"
        if titulo_especial:
            nombre_archivo_base = f"reporte_{titulo_especial.lower().replace(' ', '_')}"
            
        nombre_archivo = self.OUTPUT_DIR / f"{nombre_archivo_base}.pdf"
        doc = SimpleDocTemplate(str(nombre_archivo), pagesize=letter, 
                              leftMargin=40, rightMargin=40,
                              topMargin=60, bottomMargin=60)
        elementos = []

        # Obtener datos
        excusas = lista if lista is not None else self.excusas_repo.get_excusas(table=tabla)
        stats = self._calculate_statistics(excusas)

        # Encabezado
        titulo_reporte = titulo_especial if titulo_especial else "REPORTE DE EXCUSAS PENDIENTES"
        elementos.append(self._generate_header(titulo_reporte))
        
        # Información de generación
        elementos.extend([
            Paragraph(f"<font color='#616161'>Generado por:</font> <b>{generado_por or 'Sistema'}</b>", 
                     self.styles['HeaderText']),
            Paragraph(f"<font color='#616161'>Fecha de generación:</font> <b>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</b>", 
                     self.styles['HeaderText']),
            Spacer(1, 25)
        ])

        # Resumen ejecutivo (si aplica)
        if titulo_especial:
            elementos.extend([
                Paragraph("Resumen Ejecutivo", self.styles['SubtitleGESDE']),
                Spacer(1, 10)
            ])
            
            resumen_data = [
                ["Total de excusas:", f"{stats['total_excusas']}"],
            ]
            
            for estado, cantidad in stats['estados'].items():
                porcentaje = (cantidad / stats['total_excusas'] * 100) if stats['total_excusas'] > 0 else 0
                resumen_data.append([f"Excusas en estado '{estado}':", f"{cantidad} ({porcentaje:.1f}%)"])
            
            if stats['fecha_mas_reciente']:
                resumen_data.append(["Excusa más reciente:", f"{stats['fecha_mas_reciente'].strftime('%d/%m/%Y %H:%M:%S')}"])
            if stats['fecha_mas_antigua']:
                resumen_data.append(["Excusa más antigua:", f"{stats['fecha_mas_antigua'].strftime('%d/%m/%Y %H:%M:%S')}"])
                
            tabla_resumen = Table(resumen_data, colWidths=[200, 250])
            tabla_resumen.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#212121")),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
            ]))
            
            elementos.append(tabla_resumen)
            elementos.append(Spacer(1, 15))
            
        # Tabla principal de excusas
        data = [["ID", "PADRE", "ESTUDIANTE", "GRADO", "MOTIVO", "FECHA", "DURACIÓN", "ESTADO"]]
        
        for exc in excusas:
            data.append([
                str(exc.get('id_excuse', 'N/A')),
                str(exc.get('parent_name', 'N/A')),
                str(exc.get('student_name', 'N/A')),
                str(exc.get('grade', 'N/A')),
                str(exc.get('reason', 'N/A')),
                self._safe_strftime(exc.get('excuse_date', 'N/A')),
                str(exc.get('excuse_duration', 'N/A')),
                str(exc.get('state', 'N/A'))
            ])
        
        tabla = Table(data, colWidths=[30, 75, 75, 45, 90, 75, 60, 60], repeatRows=1)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
        ]))
        elementos.append(tabla)

        # Sección de gráficos
        if mostrar_graficos:
            elementos.extend([
                PageBreak(),
                Spacer(1, 20),
                Paragraph("Análisis Estadístico de Excusas", self.styles['ResumenTitle']),
                Spacer(1, 15)
            ])
            
            # Gráfico de estados
            estados_data = sorted(stats['estados'].items(), key=lambda x: x[1], reverse=True)
            if estados_data:
                chart_table = Table([
                    ["Distribución de Excusas por Estado"],
                    [self._create_pie_chart(estados_data, width=300, height=200)],
                    [Paragraph("Proporción de excusas según su estado actual", self.styles['ResumenText'])]
                ], colWidths=[500], rowHeights=[20, 200, 30])
                chart_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                ]))
                elementos.append(chart_table)
                elementos.append(Spacer(1, 20))
            
            # Gráfico de motivos
            if stats['top_motivos']:
                chart_table = Table([
                    ["Top 5 Motivos de Excusas"],
                    [self._create_bar_chart(stats['top_motivos'], width=400, height=200)],
                    [Paragraph("Motivos más comunes para solicitar excusas", self.styles['ResumenText'])]
                ], colWidths=[500], rowHeights=[20, 200, 30])
                chart_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                ]))
                elementos.append(chart_table)
                elementos.append(Spacer(1, 20))
            
            # Gráfico de grados
            if stats['grados']:
                chart_table = Table([
                    ["Distribución por Grado Escolar"],
                    [self._create_pie_chart(stats['grados'], width=300, height=200)],
                    [Paragraph("Proporción de excusas por grado escolar", self.styles['ResumenText'])]
                ], colWidths=[500], rowHeights=[20, 200, 30])
                chart_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                ]))
                elementos.append(chart_table)
            
            # Conclusiones
            elementos.extend([
                PageBreak(),
                Spacer(1, 15),
                Paragraph("Conclusiones y Recomendaciones", self.styles['SubtitleGESDE']),
                Spacer(1, 10),
                Paragraph("<b>Resumen del análisis:</b>", self.styles['ResumenText']),
                Spacer(1, 5),
                Paragraph(f"• Total de excusas analizadas: <b>{stats['total_excusas']}</b>", self.styles['ResumenText']),
                Spacer(1, 10),
                Paragraph("<b>Distribución por estado:</b>", self.styles['ResumenText']),
                Spacer(1, 3)
            ])
            
            for estado, cantidad in stats['estados'].items():
                porcentaje = (cantidad / stats['total_excusas'] * 100) if stats['total_excusas'] > 0 else 0
                elementos.extend([
                    Paragraph(f"• Estado '{estado}': {cantidad} excusas ({porcentaje:.1f}%)", self.styles['ResumenText']),
                    Spacer(1, 2)
                ])
            
            if stats['top_motivos']:
                elementos.extend([
                    Spacer(1, 10),
                    Paragraph("<b>Motivos más comunes:</b>", self.styles['ResumenText']),
                    Spacer(1, 3)
                ])
                for motivo, cantidad in stats['top_motivos']:
                    porcentaje = (cantidad / stats['total_excusas'] * 100) if stats['total_excusas'] > 0 else 0
                    elementos.extend([
                        Paragraph(f"• {motivo}: {cantidad} excusas ({porcentaje:.1f}%)", self.styles['ResumenText']),
                        Spacer(1, 2)
                    ])
            
            # Recomendaciones
            elementos.extend([
                Spacer(1, 10),
                Paragraph("<b>Recomendaciones:</b>", self.styles['ResumenText']),
                Spacer(1, 5)
            ])
            
            mayor_estado = max(stats['estados'].items(), key=lambda x: x[1])[0] if stats['estados'] else None
            if mayor_estado:
                elementos.append(Paragraph(
                    f"• Atención prioritaria a excusas en estado '{mayor_estado}' (mayor proporción)", 
                    self.styles['ResumenText']))
            
            if stats['top_motivos']:
                elementos.append(Paragraph(
                    f"• Establecer protocolos para el motivo más común: '{stats['top_motivos'][0][0]}'", 
                    self.styles['ResumenText']))
            
            if stats['fecha_mas_reciente'] and stats['fecha_mas_antigua']:
                dias = (stats['fecha_mas_reciente'] - stats['fecha_mas_antigua']).days
                elementos.append(Paragraph(
                    f"• Periodo analizado: {dias} días ({stats['fecha_mas_antigua'].strftime('%d/%m/%Y')} a {stats['fecha_mas_reciente'].strftime('%d/%m/%Y')})", 
                    self.styles['ResumenText']))
        
        # Pie de página
        elementos.extend([
            PageBreak(),
            Spacer(1, 20),
            Paragraph("Información del Reporte", self.styles['ResumenTitle']),
            Spacer(1, 10),
            Paragraph("Documento generado automáticamente por el sistema GESDE", self.styles['ResumenText']),
            Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}", self.styles['HeaderText']),
            Spacer(1, 20),
            Paragraph("GESDE - Gestión de Excusas Online", 
                     ParagraphStyle(name='Footer', fontSize=10, textColor=colors.HexColor("#757575")))
        ])
        
        # Generar PDF
        doc.build(elementos)
        return str(nombre_archivo)

class StudentRepository:
    def __init__(self, mysql):
        self.mysql = mysql
        
    def get_cursor(self):
        try:
            return self.mysql.connection.cursor()  # Configurado para devolver diccionarios
        except Exception as e:
            print(f"Error al obtener el cursor: {e}")
            return None
    
    def get_students(self, condition='', params=None, table='students', limit=None, offset=None):
        cursor = None
        try:
            cursor = self.get_cursor()
            if not cursor:
                return []

            # Incluimos JOIN con la tabla de usuarios para obtener información del padre
            sql = f"""
                SELECT 
                    s.id, 
                    s.name,
                    s.grade,
                    s.parent_id,
                    s.teacher_id,
                    u.name as parent_name,
                    u.phone as parent_phone
                FROM `{table}` s
                LEFT JOIN users u ON s.parent_id = u.id
                {condition}
            """
            all_params = params.copy() if params else []

            if limit is not None and offset is not None:
                sql += " LIMIT %s OFFSET %s"
                all_params += [limit, offset]

            cursor.execute(sql, all_params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
                
class ReporteEstudiantes:
    def __init__(self, student_repository):
        self.BASE_DIR = Path(__file__).parent.absolute()
        self.OUTPUT_DIR = self.BASE_DIR / "reportes" / "archivos"
        self.LOGO_PATH = Path(r"C:\Users\DUNDO\Desktop\proyectos\GESDE\src\static\ASSETS\IMG\GenericImg\GedesLogo.png")
        
        if not self.LOGO_PATH.exists():
            raise FileNotFoundError(f"Logo no encontrado en: {self.LOGO_PATH}")
        
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.student_repo = student_repository
        
        # Estilos mejorados con paleta profesional
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='TitleGESDE',
            parent=self.styles['Title'],
            fontSize=18,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1565C0"),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='SubtitleGESDE',
            parent=self.styles['Heading2'],
            fontSize=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#0D47A1"),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='ResumenTitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1976D2"),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='ResumenText',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            leftIndent=20,
            textColor=colors.HexColor("#424242")
        ))
        self.styles.add(ParagraphStyle(
            name='HeaderText',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#616161"),
            fontName='Helvetica-Oblique'
        ))

    def _safe_strftime(self, date_obj):
        if not date_obj:
            return "N/A"
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(date_obj, str):
            try:
                return datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return date_obj
        return str(date_obj)

    def _create_pie_chart(self, data, width=200, height=150):
        """Crea un gráfico circular profesional con leyenda"""
        drawing = Drawing(width, height)
        
        # Paleta de colores profesional
        colors_pie = [
            colors.HexColor("#1565C0"),  # Azul oscuro
            colors.HexColor("#42A5F5"),  # Azul medio
            colors.HexColor("#90CAF9"),  # Azul claro
            colors.HexColor("#BBDEFB"),  # Azul muy claro
            colors.HexColor("#0D47A1")   # Azul oscuro alternativo
        ]
        
        pie = Pie()
        pie.x = 20
        pie.y = 20
        pie.width = width - 40
        pie.height = height - 40
        pie.data = [d[1] for d in data]
        pie.labels = [d[0] for d in data]
        pie.sideLabels = True
        pie.simpleLabels = False
        pie.slices.strokeWidth = 0.5
        pie.slices.fontSize = 8
        pie.slices.labelRadius = 0.75
        pie.slices.popout = 5
        
        # Aplicar estilos a los segmentos
        for i, color in enumerate(colors_pie):
            if i < len(pie.slices):
                pie.slices[i].fillColor = color
                pie.slices[i].strokeColor = colors.white
                pie.slices[i].strokeWidth = 0.5
                if i == 0:
                    pie.slices[i].popout = 10
        
        # Leyenda profesional
        legend = Legend()
        legend.x = width - 100
        legend.y = height - 20
        legend.colorNamePairs = [(colors_pie[i], f"{data[i][0]} ({data[i][1]})") for i in range(len(data))]
        legend.fontName = 'Helvetica'
        legend.fontSize = 7
        legend.columnMaximum = 1
        legend.boxAnchor = 'ne'
        legend.dx = 5
        legend.dy = 5
        legend.deltax = 5
        legend.deltay = 5
        legend.autoXPadding = 5
        
        drawing.add(pie)
        drawing.add(legend)
        return drawing

    def _create_bar_chart(self, data, width=200, height=150):
        """Crea un gráfico de barras vertical profesional"""
        drawing = Drawing(width, height)
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 30
        bc.width = width - 60
        bc.height = height - 50
        bc.data = [[d[1] for d in data]]
        bc.bars.fillColor = colors.HexColor("#42A5F5")
        bc.bars.strokeColor = colors.white
        bc.bars.strokeWidth = 0.5
        
        # Configuración de ejes
        bc.categoryAxis.categoryNames = [d[0] for d in data]
        bc.categoryAxis.labels.fontName = 'Helvetica'
        bc.categoryAxis.labels.fontSize = 7
        bc.categoryAxis.labels.angle = 45
        bc.categoryAxis.labels.dy = -10
        bc.valueAxis.labels.fontName = 'Helvetica'
        bc.valueAxis.labels.fontSize = 7
        
        # Efectos visuales
        bc.barSpacing = 2
        bc.groupSpacing = 10
        bc.valueAxis.avoidBoundSpace = 5
        
        # Líneas de guía
        bc.valueAxis.gridStrokeColor = colors.HexColor("#E0E0E0")
        bc.valueAxis.gridStrokeWidth = 0.5
        
        drawing.add(bc)
        return drawing

    def generar_pdf(self, generado_por, lista=None, titulo_especial=None, mostrar_graficos=True, table='students'):
        # Configuración del documento
        # Si se especifica un título especial, úsalo en el nombre del archivo
        
        if lista is None:
            # Usar el parámetro table para obtener los estudiantes
            estudiantes = self.student_repo.get_students(table=table)
        else:
            estudiantes = lista
        nombre_archivo_base = "reporte_estudiantes"
        if titulo_especial:
            nombre_archivo_base = f"reporte_{titulo_especial.lower().replace(' ', '_')}"
            
        nombre_archivo = self.OUTPUT_DIR / f"{nombre_archivo_base}.pdf"
        doc = SimpleDocTemplate(str(nombre_archivo), pagesize=letter, 
                              leftMargin=40, rightMargin=40,
                              topMargin=60, bottomMargin=60)
        elementos = []

        # --- ENCABEZADO MEJORADO ---
        titulo_reporte = "REPORTE COMPLETO DE ESTUDIANTES"
        if titulo_especial:
            titulo_reporte = titulo_especial
            
        header_table = Table([
            [Image(self.LOGO_PATH, width=140, height=70), 
             Paragraph("<font color='#1565C0'><b>GESDE</b></font> - Gestión de Excusas Online<br/>"
                      f"<font size=14 color='#0D47A1'>{titulo_reporte}</font>", 
                      self.styles['TitleGESDE'])]
        ], colWidths=[160, 340])
        
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#E3F2FD"))
        ]))
        
        elementos.append(header_table)
        
        # Información de generación
        elementos.extend([
            Paragraph(f"<font color='#616161'>Generado por:</font> <b>{generado_por or 'Sistema'}</b>", 
                     self.styles['HeaderText']),
            Paragraph(f"<font color='#616161'>Fecha de generación:</font> <b>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</b>", 
                     self.styles['HeaderText']),
            Spacer(1, 25)
        ])

        # --- RESUMEN EJECUTIVO AL INICIO (si se requiere) ---
        if titulo_especial and "POR GRADO" in titulo_especial.upper():
            elementos.extend([
                Paragraph("Resumen Ejecutivo", self.styles['SubtitleGESDE']),
                Spacer(1, 10)
            ])
            
            # Usar la lista proporcionada o recuperar todos los estudiantes si no se proporciona
            if lista is None:
                estudiantes = self.student_repo.get_students(table='students')
            else:
                estudiantes = lista
                
            total_estudiantes = len(estudiantes)
            
            # Extraer estadísticas específicas por grado
            grados = {}
            for estudiante in estudiantes:
                grado = estudiante.get('grade', 'No definido')
                grados[grado] = grados.get(grado, 0) + 1
            
            # Tabla de resumen
            resumen_data = [
                ["Total de estudiantes:", f"{total_estudiantes}"]
            ]
            
            for grado, cantidad in sorted(grados.items()):
                porcentaje = (cantidad / total_estudiantes * 100) if total_estudiantes > 0 else 0
                resumen_data.append([f"Estudiantes en {grado}:", f"{cantidad} ({porcentaje:.1f}%)"])
                
            tabla_resumen = Table(resumen_data, colWidths=[200, 250])
            tabla_resumen.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#212121")),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0"))
            ]))
            
            elementos.append(tabla_resumen)
            elementos.append(Spacer(1, 15))
            
        # --- TABLA DE ESTUDIANTES ---
        # Usar la lista proporcionada o recuperar todos los estudiantes si no se proporciona
        if lista is None:
            estudiantes = self.student_repo.get_students(table='students')
        else:
            estudiantes = lista
        
        # Preparar tabla
        encabezados = ["ID", "NOMBRE", "GRADO", "PADRE/TUTOR", "TELÉFONO DE CONTACTO"]
        data = [encabezados]
        
        for estudiante in estudiantes:
            row = [
                str(estudiante.get('id', 'N/A')),
                str(estudiante.get('name', 'N/A')),
                str(estudiante.get('grade', 'N/A')),
                str(estudiante.get('parent_name', 'N/A')),
                str(estudiante.get('parent_phone', 'N/A'))
            ]
            data.append(row)
        
        tabla = Table(data, colWidths=[40, 150, 80, 130, 100], repeatRows=1)
        
        estilo_tabla = TableStyle([
            # Cabecera
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Cuerpo
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#212121")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ])
        
        tabla.setStyle(estilo_tabla)
        elementos.append(tabla)
        
        # --- SECCIÓN DE GRÁFICOS ---
        # Solo mostrar gráficos si mostrar_graficos es True
        if mostrar_graficos:
            elementos.extend([
                PageBreak(),
                Spacer(1, 20),
                Paragraph("Análisis Estadístico de Estudiantes", self.styles['ResumenTitle']),
                Spacer(1, 15)
            ])
            
            # Estadísticas
            total_estudiantes = len(estudiantes)
            
            # Distribución por grado
            grados = {}
            for estudiante in estudiantes:
                grado = estudiante.get('grade', 'No definido')
                grados[grado] = grados.get(grado, 0) + 1
            
            grados_sorted = sorted(grados.items())
            
            # Análisis de contacto con padres
            con_telefono = sum(1 for estudiante in estudiantes if estudiante.get('parent_phone') and estudiante.get('parent_phone') not in ['N/A', ''])
            sin_telefono = total_estudiantes - con_telefono
            
            telefono_data = [
                ("Con contacto", con_telefono),
                ("Sin contacto", sin_telefono)
            ]
            
            # Gráficos
            if grados_sorted:
                bar_chart_grados = self._create_bar_chart(grados_sorted, width=400, height=200)
                
                # Tabla para organizar el gráfico
                chart_table = Table([
                    ["Distribución de Estudiantes por Grado"],
                    [bar_chart_grados],
                    [Paragraph("Este gráfico muestra la cantidad de estudiantes por cada grado", 
                              self.styles['ResumenText'])]
                ], colWidths=[500], rowHeights=[20, 200, 30])
                
                chart_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                    ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
                    ('FONTSIZE', (0, 2), (-1, 2), 9)
                ]))
                
                elementos.append(chart_table)
                elementos.append(Spacer(1, 20))
            
            # Gráfico de contacto
            if telefono_data[0][1] > 0 or telefono_data[1][1] > 0:
                pie_contacto = self._create_pie_chart(telefono_data, width=300, height=200)
                
                chart_table = Table([
                    ["Estudiantes con Información de Contacto"],
                    [pie_contacto],
                    [Paragraph("Proporción de estudiantes con y sin información de contacto de padres/tutores",
                              self.styles['ResumenText'])]
                ], colWidths=[500], rowHeights=[20, 200, 30])
                
                chart_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                    ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
                    ('FONTSIZE', (0, 2), (-1, 2), 9)
                ]))
                
                elementos.append(chart_table)
                elementos.append(Spacer(1, 20))
            
            # --- RESUMEN FINAL ---
            elementos.extend([
                PageBreak(),
                Spacer(1, 15),
                Paragraph("Resumen Final", self.styles['SubtitleGESDE']),
                Spacer(1, 10)
            ])
            
            # Detalles estadísticos
            resumen_content = [
                Paragraph(f"<b>Total de estudiantes registrados:</b> {total_estudiantes}", self.styles['ResumenText']),
                Spacer(1, 5),
                Paragraph("<b>Distribución por grados:</b>", self.styles['ResumenText'])
            ]
            
            for grado, cantidad in grados_sorted:
                porcentaje = (cantidad / total_estudiantes) * 100 if total_estudiantes > 0 else 0
                resumen_content.extend([
                    Paragraph(f"• {grado}: {cantidad} estudiantes ({porcentaje:.1f}%)", 
                             self.styles['ResumenText']),
                    Spacer(1, 3)
                ])
            
            # Estadísticas de contacto
            porcentaje_con_contacto = (con_telefono / total_estudiantes) * 100 if total_estudiantes > 0 else 0
            resumen_content.extend([
                Spacer(1, 10),
                Paragraph(f"<b>Estudiantes con información de contacto:</b> {con_telefono} ({porcentaje_con_contacto:.1f}%)", 
                         self.styles['ResumenText']),
                Paragraph(f"<b>Estudiantes sin información de contacto:</b> {sin_telefono} ({100-porcentaje_con_contacto:.1f}%)", 
                         self.styles['ResumenText']),
                Spacer(1, 10)
            ])
            
            # Recomendaciones
            resumen_content.extend([
                Paragraph("<b>Recomendaciones:</b>", self.styles['ResumenText']),
                Spacer(1, 5)
            ])
            
            if porcentaje_con_contacto < 90:
                resumen_content.append(
                    Paragraph("• Se recomienda completar la información de contacto de los padres/tutores para mejorar la comunicación.", 
                             self.styles['ResumenText'])
                )
            
            elementos.extend(resumen_content)
        
        # --- PIE DE PÁGINA ---
        elementos.append(PageBreak())
        elementos.extend([
            Spacer(1, 20),
            Paragraph("Información del Reporte", self.styles['ResumenTitle']),
            Spacer(1, 10),
            Paragraph("Este documento fue generado automáticamente por el sistema GESDE", self.styles['ResumenText']),
            Paragraph("Los datos reflejan el estado actual al momento de generación", self.styles['ResumenText']),
            Spacer(1, 5),
            Paragraph(f"Documento generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}", 
                     self.styles['HeaderText']),
            Spacer(1, 10),
            Paragraph("GESDE - Gestión de Excusas Online", 
                     ParagraphStyle(name='Footer', fontSize=10, textColor=colors.HexColor("#757575")))
        ])
        
        # Generar PDF
        doc.build(elementos)
        return str(nombre_archivo)
    
@report_bp.route('/reporte/reporte_estudiantes', methods=['GET'])
def descargar_reporte_estudiantes():
    try:
        # 1. Crea el repositorio primero
        student_repo = StudentRepository(mysql)
        
        # 2. Pasa el repositorio
        generador = ReporteEstudiantes(student_repo)
        
        # 3. Genera el PDF
        pdf_path = generador.generar_pdf(session.get('username'))
        
        # 4. Envía el archivo
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="reporte_estudiantes.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error al generar el reporte: {str(e)}", 500

# Ejemplo de uso con Flask
@report_bp.route('/reporte/excusas_pendientes', methods=['GET'])
def descargar_reporte_excusas(tabla='pending_excuses'):
    try:
        # 1. Crea el repositorio primero
        excusas_repo = ExcusasRepository(mysql)
        
        # 2. Pasa el repositorio
        generador = ReporteExcusasPendientes(excusas_repo)
        
        # 3. Genera el PDF
        pdf_path = generador.generar_pdf(
            generado_por=session.get('username'),
            tabla=tabla
        )
        
        # 4. Envía el archivo
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="reporte_excusas_pendientes.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error al generar el reporte: {str(e)}", 500

@report_bp.route('/reporte/excusas_aprobadas', methods=['GET'])
def descargar_reporte_excusas_aprobadas(tabla='accepted_excuses'):
    try:
        # 1. Crea el repositorio primero
        excusas_repo = ExcusasRepository(mysql)
        
        # 2. Pasa el repositorio
        generador = ReporteExcusasPendientes(excusas_repo)
        
        # 3. Genera el PDF
        pdf_path = generador.generar_pdf(
            generado_por=session.get('username'),
            tabla=tabla
        )
        
        # 4. Envía el archivo
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="reporte_excusas_aprobadas.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error al generar el reporte: {str(e)}", 500

@report_bp.route('/reporte/excusas_rechazadas', methods=['GET'])
def descargar_reporte_excusas_rechazadas(tabla='rejected_excuses'):
        try:
            if session.get('rol') not in ['admin', 'secretary', 'teacher']:
                return jsonify({"error": "No autorizado"}), 403
            
            # 1. Crea el repositorio primero
            excusas_repo = ExcusasRepository(mysql)
            
            # 2. Pasa el repositorio
            generador = ReporteExcusasPendientes(excusas_repo)
            
            # 3. Genera el PDF con título especial para excusas aprobadas
            pdf_path = generador.generar_pdf(
                generado_por=session.get('username'),
                tabla=tabla,
                titulo_especial="REPORTE DE EXCUSAS RECHAZADAS"
            )
            
            # 4. Envía el archivo
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name="reporte_excusas_rechazadas.pdf",
                mimetype='application/pdf'
            )
        except Exception as e:
            current_app.logger.error(f"Error al generar reporte de excusas rechazadas: {str(e)}")
            return jsonify({"error": f"Error al generar el reporte: {str(e)}"}), 500

@report_bp.route('/reporte/usuarios-activos')
def descargar_reporte_usuarios():
    try:
        # 1. Crea el repositorio primero
        user_repo = UserRepository(mysql)
        
        # 2. Pasa el repositorio (no la conexión mysql directamente)
        generador = ReporteTodosUsuarios(user_repo)
        
        # 3. Genera el PDF
        pdf_path = generador.generar_pdf(session.get('username'))
        
        # 4. Envía el archivo
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="reporte_usuarios.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error al generar el reporte: {str(e)}", 500
    
@report_bp.route('/reporte/usuarios_deshabilitados', methods=['GET'])
def descargar_reporte_usuarios_deshabilitados():
    try:
        if session.get('rol') not in ['admin', 'secretary']:
            return jsonify({"error": "No autorizado"}), 403

        # 1. Obtener usuarios deshabilitados primero
        user_repo = UserRepository(mysql)
        usuarios = user_repo.get_users(table='userunbailited')  # Asumiendo que get_usuarios acepta table
        
        # 2. Generar reporte pasando la lista directamente
        generador = ReporteTodosUsuarios(user_repo)
        pdf_path = generador.generar_pdf(
            generado_por=session.get('username'),
            lista=usuarios,  # Pasamos los usuarios ya obtenidos
            titulo_especial="REPORTE DE USUARIOS DESHABILITADOS"
        )
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="reporte_usuarios_deshabilitados.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        current_app.logger.error(f"Error al generar reporte: {str(e)}")
        return jsonify({"error": f"Error al generar el reporte: {str(e)}"}), 500
      
@report_bp.route('/reporte/padres')
def descargar_reporte_padres():
    try:
        if session.get('rol') not in ['admin', 'secretary']:
            return jsonify({"error": "No tienes permisos para ver este reporte"}), 403

        # Crear repositorio y obtener usuarios padres
        user_repo = UserRepository(mysql)
        padres = user_repo.get_users(condition="WHERE rol = %s", params=['parent'])

        if not padres:
            return jsonify({"error": "No se encontraron padres registrados"}), 404

        # Generar el PDF
        generador = ReporteTodosUsuarios(user_repo)
        pdf_path = generador.generar_pdf(
            generado_por=session.get('username'),
            lista=padres,  # Ahora la lista será utilizada correctamente
            titulo_especial="REPORTE DE PADRES",
            mostrar_graficos=True  # Cambiado a True para mostrar los gráficos
        )

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"reporte_padres_{datetime.now().strftime('%Y%m%d')}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        current_app.logger.error(f"Error generando reporte de padres: {str(e)}", exc_info=True)
        return jsonify({"error": "Error al generar el reporte", "detalle": str(e)}), 500

@report_bp.route('/reporte/trabajadores')
def descargar_reporte_trabajadores():
    try:
        if session.get('rol') not in ['admin', 'secretary']:
            return jsonify({"error": "No tienes permisos para ver este reporte"}), 403

        # Crear repositorio y obtener usuarios que no sean padres
        user_repo = UserRepository(mysql)
        trabajadores = user_repo.get_users(condition="WHERE rol != %s", params=['parent'])

        if not trabajadores:
            return jsonify({"error": "No se encontraron trabajadores registrados"}), 404

        # Generar el PDF con gráficos activados
        generador = ReporteTodosUsuarios(user_repo)
        pdf_path = generador.generar_pdf(
            generado_por=session.get('username'),
            lista=trabajadores,
            titulo_especial="REPORTE DE TRABAJADORES",
            mostrar_graficos=True  # Activamos los gráficos
        )

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"reporte_trabajadores_{datetime.now().strftime('%Y%m%d')}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        current_app.logger.error(f"Error generando reporte de trabajadores: {str(e)}", exc_info=True)
        return jsonify({"error": "Error al generar el reporte", "detalle": str(e)}), 500
