import os
from datetime import timedelta
from cryptography.fernet import Fernet

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FERNET_KEY = os.environ.get("FERNET_KEY") or Fernet.generate_key()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "microfinance.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ENCRYPTION_KEY = FERNET_KEY

    # ===== SMS =====
    SMS_ENABLED = False
    TWILIO_ACCOUNT_SID = ""
    TWILIO_AUTH_TOKEN = ""
    TWILIO_PHONE = ""

    # ===== MTN MOMO (UGANDA) =====
    MTN_COLLECTION_KEY = ""
    MTN_COLLECTION_SECRET = ""
    MTN_SUBSCRIPTION_KEY = ""
    MTN_BASE_URL = "https://sandbox.momodeveloper.mtn.com"

    # ===== AIRTEL =====
    AIRTEL_CLIENT_ID = ""
    AIRTEL_CLIENT_SECRET = ""
    AIRTEL_BASE_URL = "https://openapi.airtel.africa"

    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)