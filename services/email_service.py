from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_challenge_email(receiver_email, sender_name, quiz_link):
    with current_app.app_context():
        msg = Message(
            subject=f"You've been challenged by {sender_name}!",
            recipients=[receiver_email],
            html=f"""
            <h1>Quiz Challenge!</h1>
            <p>{sender_name} has challenged you to beat their quiz score!</p>
            <p><a href="{quiz_link}">Click here to take the challenge!</a></p>
            """,
            sender=current_app.config['MAIL_USERNAME']
        )
        mail.send(msg)