from cryptography.fernet import Fernet
from datetime import datetime
from config import Config

cipher = Fernet(Config.ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()

def calculate_overdue_days(due_date):
    today = datetime.utcnow()
    return max((today - due_date).days, 0) if today > due_date else 0

def apply_daily_penalty(loan):
    overdue_days = calculate_overdue_days(loan.due_date)
    if overdue_days <= 0:
        return 0
    penalty = loan.balance * loan.daily_penalty * overdue_days
    loan.balance += penalty
    return penalty

# ===== MTN MOMO =====
import requests, uuid, base64

def mtn_request_to_pay(phone, amount):
    ref_id = str(uuid.uuid4())
    url = Config.MTN_BASE_URL + "/collection/v1_0/requesttopay"

    headers = {
        "X-Reference-Id": ref_id,
        "X-Target-Environment": "sandbox",
        "Ocp-Apim-Subscription-Key": Config.MTN_SUBSCRIPTION_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "amount": str(amount),
        "currency": "UGX",
        "externalId": ref_id,
        "payer": {"partyIdType": "MSISDN", "partyId": phone},
        "payerMessage": "Loan repayment",
        "payeeNote": "Microfinance"
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        return {"status": r.status_code, "ref": ref_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ===== AIRTEL =====

def airtel_request_to_pay(phone, amount):
    url = Config.AIRTEL_BASE_URL + "/merchant/v1/payments/"
    payload = {"reference": "loan", "subscriber": {"country": "UG", "currency": "UGX", "msisdn": phone}, "transaction": {"amount": amount}}
    try:
        r = requests.post(url, json=payload, timeout=30)
        return {"status": r.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}