from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
from flask_mail import Message
from . import mail  # mail initialized in app/__init__.py

def generate_reset_token(email: str) -> str:
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])

def verify_reset_token(token: str, expiration: int = 3600):
    """Returns email if token is valid within `expiration` seconds, else None."""
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
        return email
    except Exception:
        return None

def send_reset_email(user_email: str):
    try:
        token = generate_reset_token(user_email)
        reset_url = url_for("main.reset_with_token", token=token, _external=True)

        subject = "🔐 Reset your password – BhavDoc"
        body = f"""Hi,

We received a request to reset your password on BhavDoc.

Click the link below to set a new password (valid for 1 hour):
{reset_url}

If you didn’t request this, please ignore this email.

— BhavDoc Management System
Designed & Developed by Bhavesh Jha
"""
        msg = Message(subject=subject, recipients=[user_email], body=body)
        mail.send(msg)

        print("✅ Email sent successfully to:", user_email)
        return True
    except Exception as e:
        print("❌ Email send failed:", str(e))  # 👈 Console pe exact error dikhayega
        return False
