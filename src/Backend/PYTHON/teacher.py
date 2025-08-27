from flask import render_template, request, session, Blueprint
from login import mysql
from datetime import datetime, timedelta

teacher_excuses_bp = Blueprint('teacher', __name__, template_folder='../templates')


class Database:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_connection(self):
        try:
            return self.mysql.connection.cursor()
        except Exception as err:
            print(f"Error: {err}")
            return None


class TeacherExcuses:
    def __init__(self, db, teacher_id):
        self.db = db
        self.teacher_id = teacher_id

    def get_all_excuses(self):
        try:
            cursor = self.db.get_connection()
            sql = """
            SELECT 
              ae.id_excuse, ae.parent_name, ae.student_name, ae.grade, ae.reason,
              DATE(ae.excuse_date) AS excuse_date, ae.excuse_duration, ae.specification
            FROM accepted_excuses ae
            INNER JOIN teacher_schedule ts
              ON ts.grade = ae.grade
             AND ts.teacher_id = %s
            """
            cursor.execute(sql, (self.teacher_id,))
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"[ERROR get_all_excuses] {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_excuses_for_date(self, target_date: datetime.date):
        records = self.get_all_excuses()

        processed = []
        for r in records:
            duration_text = (r.get('excuse_duration') or '').strip().lower()

            # Determinar duración
            if duration_text.startswith('indefin'):
                days = ['indefinido']
                include = True  # Mostrar siempre
            else:
                try:
                    num_days = int(duration_text.split()[0])
                except (ValueError, IndexError):
                    num_days = 1

                start_date = r['excuse_date']
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

                # Verificar si el target_date está dentro del rango
                end_date = start_date + timedelta(days=num_days - 1)
                include = start_date <= target_date <= end_date

                # Para mostrar los días afectados
                days = []
                for i in range(num_days):
                    d = start_date + timedelta(days=i)
                    days.append(d.strftime('%A').lower())

            if include:
                r['days'] = days
                processed.append(r)

        return processed

    def get_paginated_excuses(self, page, per_page, target_date):
        try:
            all_excuses = self.get_excuses_for_date(target_date)
            total = len(all_excuses)
            start = (page - 1) * per_page
            end = start + per_page
            return {
                'excuses': all_excuses[start:end],
                'page': page,
                'has_prev': page > 1,
                'has_next': end < total,
                'total_accepted': total
            }
        except Exception as e:
            print(f"[ERROR get_paginated_excuses] {e}")
            return {
                'excuses': [],
                'page': page,
                'has_prev': False,
                'has_next': False,
                'total_accepted': 0
            }


@teacher_excuses_bp.route('/teacher')
def show_excuses():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 9
        teacher_id = session.get('user_id')

        # Fecha objetivo desde la URL o fecha actual
        date_str = request.args.get('date')
        if date_str:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            target_date = datetime.now().date()

        db = Database(mysql)
        handler = TeacherExcuses(db, teacher_id)
        data = handler.get_paginated_excuses(page, per_page, target_date)

        print("Excusas para", target_date, ":", data["excuses"])

        return render_template('teacher/teacher.html', **data, selected_date=target_date)

    except Exception as e:
        print(f"[ERROR show_excuses] {e}")
        return "Error al mostrar las excusas.", 500
