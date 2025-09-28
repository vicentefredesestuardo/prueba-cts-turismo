from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Contestant

def _send_html_email(subject, text, html, to):
    """
    Helper para enviar emails HTML con texto alternativo.
    
    Args:
        subject (str): Asunto del email
        text (str): Versión de texto plano del mensaje
        html (str): Versión HTML del mensaje
        to (str): Email del destinatario
    """
    from_email = f"{settings.HOTEL_NAME} <{settings.DEFAULT_FROM_EMAIL}>"
    msg = EmailMultiAlternatives(subject, text, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()

@shared_task
def send_verification_email(contestant_id, token):
    """
    Envía email de verificación a un concursante con HTML y texto alternativo.
    
    Args:
        contestant_id (int): ID del concursante en la base de datos
        token (str): Token UUID para verificación de email
    
    Returns:
        None: Tarea asíncrona de Celery
    """
    try:
        c = Contestant.objects.get(id=contestant_id)
        verification_url = f"{settings.FRONTEND_URL}/verify?token={token}"
        
        subject = f"[{settings.HOTEL_NAME}] Verifica tu email – Concurso San Valentín"
        text = f"Hola {c.full_name}\n\nPara participar en el concurso de San Valentín del {settings.HOTEL_NAME}, verifica tu correo: {verification_url}\n(Este enlace expira en 2 horas)"
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; text-align: center;">
            <h2 style="color: #e91e63;">¡Hola {c.full_name}!</h2>
            <p>¡Gracias por inscribirte en el concurso de San Valentín del <strong>{settings.HOTEL_NAME}</strong>!</p>
            <p>Para completar tu registro y participar en el sorteo, haz clic en el siguiente botón:</p>
            <div style="text-align: center; margin: 30px 0;">
            <a href="{verification_url}" style="background-color: #e91e63; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Verificar mi cuenta
            </a>
            </div>
            <p><small style="color: #666;">Este enlace expira en 2 horas.</small></p>
            <p>¡Buena suerte!<br><strong>{settings.HOTEL_NAME}</strong></p>
        </div>
        """
        
        _send_html_email(subject, text, html, c.email)
        
    except Exception as e:
        print(f"Error enviando email de verificación: {e}")

@shared_task
def send_winner_notification(contestant_id):
    """
    Envía notificación de ganador a un concursante con HTML y texto alternativo.
    
    Args:
        contestant_id (int): ID del concursante ganador en la base de datos
    
    Returns:
        None: Tarea asíncrona de Celery
    """
    try:
        c = Contestant.objects.get(id=contestant_id)
        
        subject = f"🎉 ¡FELICIDADES! Eres el ganador – {settings.HOTEL_NAME}"
        text = f"¡Hola {c.full_name}!\n\n¡Felicitaciones! Eres el ganador del concurso de San Valentín del {settings.HOTEL_NAME}.\nTe contactaremos pronto para coordinar tu premio."
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; text-align: center;">
            <h1 style="color: #e91e63;">🎉 ¡FELICIDADES! 🎉</h1>
            <h2>¡Hola {c.full_name}!</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p style="font-size: 18px;"><strong>¡Has sido seleccionado como el GANADOR del concurso de San Valentín del <strong>{settings.HOTEL_NAME}</strong>!</strong></p>
                <p style="font-size: 16px; color: #e91e63;"><strong>🏆 Tu premio: 2 noches románticas en nuestro hotel</strong></p>
            </div>
            <p>Nos pondremos en contacto contigo pronto para coordinar todos los detalles.</p>
            <p>¡Disfruta tu premio!<br><strong>{settings.HOTEL_NAME}</strong><br><em>Escápate con estilo</em></p>
        </div>
        """
        
        _send_html_email(subject, text, html, c.email)
        
    except Exception as e:
        print(f"Error enviando email al ganador: {e}")