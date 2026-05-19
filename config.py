import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-change-me")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "change-this-salt")

    # --- Gmail SMTP (use App Password) ---
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # your@gmail.com
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # 16-char app password
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", os.environ.get("MAIL_USERNAME"))
