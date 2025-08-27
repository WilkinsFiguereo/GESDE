from flask import request, jsonify, Blueprint
from twilio.rest import Client

notification_bp = Blueprint('notification', __name__, template_folder='../templates')

# Configuración de Twilio
account_sid = "AC0c60b0f4c2b82eda97f8259d47423412"
auth_token = "6e9ad64fa6d18f9d89a2321751aa47af"

if not account_sid or not auth_token:
    raise ValueError("Las credenciales de Twilio no están configuradas correctamente.")

# Número de WhatsApp de Twilio
twilio_whatsapp_number = 'whatsapp:+14155238886'

# Inicialización del cliente de Twilio
client = Client(account_sid, auth_token)


def send_whatsapp_message(to, message):
    """ Envía un mensaje de WhatsApp usando Twilio. """
    try:
        # Enviando el mensaje
        message = client.messages.create(
            body=message,
            from_=twilio_whatsapp_number,  # Número de Twilio que debe estar habilitado
            to=f'whatsapp:{to}'  # Número de destino al que se enviará el mensaje
        )
        return message.sid
    except Exception as e:
        # Capturando cualquier error que ocurra al enviar el mensaje
        print(f"Error al enviar el mensaje: {e}")
        raise e  # Volver a lanzar la excepción para manejarla a nivel superior

@notification_bp.route('/excuse/<int:excuse_id>/update', methods=['POST'])
def update_excuse(excuse_id):
    """ 
    Ruta que actualiza el estado de una excusa y notifica al usuario vía WhatsApp.
    """
    data = request.get_json()  # Obtiene la data del JSON en el cuerpo de la solicitud
    status = data.get('status')  # Obtiene el estado de la excusa (aceptada o rechazada)

    if status not in ['accepted', 'rejected']:  # Verifica que el estado sea válido
        return jsonify({'error': 'Estado no válido. Usa "accepted" o "rejected".'}), 400

    # Usando el número por defecto (deberías obtenerlo de la base de datos si es dinámico)
    user_phone = '+1 849 880 9890'

    # Define el mensaje basado en el estado
    message_text = 'Tu excusa ha sido aceptada.' if status == 'accepted' else 'Tu excusa ha sido rechazada.'

    try:
        # Llamamos a la función para enviar el mensaje por WhatsApp
        message_sid = send_whatsapp_message(user_phone, message_text)
    except Exception as e:
        # Si hay algún error, devuelve el mensaje de error
        return jsonify({'error': str(e)}), 500

    # Devuelve un mensaje de éxito con el SID del mensaje enviado
    return jsonify({
        'message': 'Estado actualizado y notificación enviada.',
        'message_sid': message_sid
    }), 200
