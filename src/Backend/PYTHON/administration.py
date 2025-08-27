from flask import Blueprint, render_template, redirect, url_for, flash, request
from login import mysql
from notification import send_whatsapp_message

class ExcuseManager:
    def __init__(self, mysql):
        self.mysql = mysql
        self.pending_excuses_bp = Blueprint('pending', __name__, template_folder='../templates')
        self.accept_excuse_bp = Blueprint('accept', __name__, template_folder='../templates')
        self.rejected_excuses_bp = Blueprint('rejected', __name__, template_folder='../templates')
        self.register_routes()
        self.register_context_processors()

    def inject_totals(self):
        try:
            cursor = self.mysql.connection.cursor()

            # Obtener el total de excusas pendientes
            cursor.execute("SELECT COUNT(*) AS total_excuses FROM pending_excuses")
            total_excuses = cursor.fetchone()["total_excuses"]

            # Obtener el total de excusas aceptadas
            cursor.execute("SELECT COUNT(*) AS total_accepted FROM accepted_excuses")
            total_accepted = cursor.fetchone()["total_accepted"]

            # Obtener el total de excusas rechazadas
            cursor.execute("SELECT COUNT(*) AS total_rejected FROM rejected_excuses")
            total_rejected = cursor.fetchone()["total_rejected"]

            return {
                'total_excuses': total_excuses,
                'total_accepted': total_accepted,
                'total_rejected': total_rejected
            }
        except Exception as e:
            print(f"Error al obtener los totales: {e}")
            return {
                'total_excuses': 0,
                'total_accepted': 0,
                'total_rejected': 0
            }
        finally:
            cursor.close()

    def register_context_processors(self):
        @self.pending_excuses_bp.context_processor
        def inject_totals_pending():
            return self.inject_totals()

        @self.accept_excuse_bp.context_processor
        def inject_totals_accept():
            return self.inject_totals()

        @self.rejected_excuses_bp.context_processor
        def inject_totals_rejected():
            return self.inject_totals()

    def register_routes(self):
        @self.pending_excuses_bp.route('/pending')
        def pending():
            try:
                page = request.args.get('page', 1, type=int)
                per_page = 10
                offset = (page - 1) * per_page

                cursor = self.mysql.connection.cursor()

                cursor.execute("SELECT COUNT(*) AS total FROM pending_excuses")
                total_result = cursor.fetchone()
                total_excuses = total_result['total'] if total_result else 0

                query = """
                    SELECT 
                        id_excuse, parent_name, student_name, grade, reason, 
                        DATE(excuse_date) AS excuse_date, excuse_duration, specification 
                    FROM pending_excuses
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (per_page, offset))
                pendings = cursor.fetchall()

                has_prev = page > 1
                has_next = offset + per_page < total_excuses

                return render_template(
                    'administration/pending_excuses.html', 
                    pendings=pendings, 
                    page=page, 
                    has_prev=has_prev, 
                    has_next=has_next,
                    total_excuses=total_excuses
                )
            except Exception as e:
                print(f"Error al obtener usuarios: {e}")
                return render_template('administration/pending_excuses.html', pendings=[])
            finally:
                cursor.close()

        @self.pending_excuses_bp.route('/pending/accept/<int:user_id>', methods=['POST'])
        def accept_excuse(user_id):
            try:
                cursor = self.mysql.connection.cursor()
                cursor.execute('SELECT * FROM pending_excuses WHERE id_excuse = %s', (user_id,))
                excuse = cursor.fetchone()

                if not excuse:
                    flash('Excusa no encontrada.', 'warning')
                    return redirect(url_for('pending.pending'))

                cursor.execute(
                    '''INSERT INTO accepted_excuses (id_excuse, parent_name, student_name, grade, reason, id_user, excuse_date, excuse_duration, specification, file_data, file_extension, state) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (excuse["id_excuse"], excuse["parent_name"], excuse["student_name"], excuse["grade"], excuse["reason"], excuse["id_user"], excuse["excuse_date"], excuse["excuse_duration"], excuse["specification"], excuse["file_data"], excuse["file_extension"], "Aprobado")
                )

                cursor.execute('DELETE FROM pending_excuses WHERE id_excuse = %s', (user_id,))
                self.mysql.connection.commit()
                flash(f'Excusa {user_id} aceptada con éxito.', 'success')

                try:
                    message_sid = send_whatsapp_message('+18498809890', '¡Buen día! Nos complace informarte que tu excusa ha sido aceptada. Si tienes alguna pregunta o necesitas más detalles, no dudes en contactarnos.')
                    flash(f'Notificación enviada (SID: {message_sid}).', 'info')
                except Exception as e:
                    flash(f'Error al enviar notificación: {e}', 'danger')
            except Exception as e:
                self.mysql.connection.rollback()
                flash(f'Error al aceptar la excusa: {e}', 'danger')
            finally:
                cursor.close()

            return redirect(url_for('pending.pending'))

        @self.pending_excuses_bp.route('/pending/reject/<int:user_id>', methods=['POST'])
        def rejected_excuse(user_id):
            try:
                cursor = self.mysql.connection.cursor()
                cursor.execute('SELECT * FROM pending_excuses WHERE id_excuse = %s', (user_id,))
                excuse = cursor.fetchone()

                if not excuse:
                    flash('Excusa no encontrada.', 'warning')
                    return redirect(url_for('pending.pending'))

                cursor.execute(
                    '''INSERT INTO rejected_excuses (id_excuse, parent_name, student_name, grade, reason, id_user, excuse_date, excuse_duration, specification, file_data, file_extension, state) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (excuse["id_excuse"], excuse["parent_name"], excuse["student_name"], excuse["grade"], excuse["reason"], excuse["id_user"], excuse["excuse_date"], excuse["excuse_duration"], excuse["specification"], excuse["file_data"], excuse["file_extension"], "Rechazado")
                )

                cursor.execute('DELETE FROM pending_excuses WHERE id_excuse = %s', (user_id,))
                self.mysql.connection.commit()
                flash(f'Excusa {user_id} rechazada con éxito.', 'success')

                try:
                    message_sid = send_whatsapp_message('+18498809890', 'Estimado/a, lamentablemente su excusa ha sido rechazada. Si necesita más información o desea discutir el asunto, por favor, no dude en ponerse en contacto con la administraccion.')
                    flash(f'Notificación enviada (SID: {message_sid}).', 'info')
                except Exception as e:
                    flash(f'Error al enviar notificación: {e}', 'danger')
            except Exception as e:
                self.mysql.connection.rollback()
                print(f'Error al rechazar la excusa: {e}', 'danger')
            finally:
                cursor.close()

            return redirect(url_for('pending.pending'))

        @self.accept_excuse_bp.route('/accept')
        def accept():
            try:
                page = request.args.get('page', 1, type=int)
                per_page = 10
                offset = (page - 1) * per_page

                cursor = self.mysql.connection.cursor()

                cursor.execute("SELECT COUNT(*) AS total FROM accepted_excuses")
                total_result = cursor.fetchone()
                total_accepted = total_result['total'] if total_result else 0

                query = """
                    SELECT 
                        id_excuse, parent_name, student_name, grade, reason, 
                        DATE(excuse_date) AS excuse_date, excuse_duration, specification 
                    FROM accepted_excuses
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (per_page, offset))
                accepted = cursor.fetchall()

                has_prev = page > 1
                has_next = offset + per_page < total_accepted

                return render_template(
                    'administration/accepted_excuse.html', 
                    accept=accepted, 
                    page=page, 
                    has_prev=has_prev, 
                    has_next=has_next,
                    total_accepted=total_accepted
                )
            except Exception as e:
                print(f"Error al obtener usuarios: {e}")
                return render_template('administration/accepted_excuse.html', accept=[])
            finally:
                cursor.close()

        @self.rejected_excuses_bp.route('/rejected')
        def rejected():
            try:
                page = request.args.get('page', 1, type=int)
                per_page = 10
                offset = (page - 1) * per_page

                cursor = self.mysql.connection.cursor()

                cursor.execute("SELECT COUNT(*) AS total FROM rejected_excuses")
                total_result = cursor.fetchone()
                total_rejected = total_result['total'] if total_result else 0

                query = """
                    SELECT 
                        id_excuse, parent_name, student_name, grade, reason, 
                        DATE(excuse_date) AS excuse_date, excuse_duration, specification 
                    FROM rejected_excuses
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (per_page, offset))
                rejected = cursor.fetchall()

                has_prev = page > 1
                has_next = offset + per_page < total_rejected

                return render_template(
                    'administration/rejected_excuses.html', 
                    rejected=rejected, 
                    page=page, 
                    has_prev=has_prev, 
                    has_next=has_next,
                    total_rejected=total_rejected
                )
            except Exception as e:
                print(f"Error al obtener usuarios: {e}")
                return render_template('administration/rejected_excuses.html', rejected=[], page=1, has_prev=False, has_next=False, total_rejected=0)
            finally:
                cursor.close()

# Uso de la clase
excuse_manager = ExcuseManager(mysql)
pending_excuses_bp = excuse_manager.pending_excuses_bp
accept_excuse_bp = excuse_manager.accept_excuse_bp
rejected_excuses_bp = excuse_manager.rejected_excuses_bp