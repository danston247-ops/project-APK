from apscheduler.schedulers.background import BackgroundScheduler
from models import db, Loan, Client
from utils import apply_daily_penalty
from app import app, send_sms

scheduler = BackgroundScheduler()


def daily_jobs():
    with app.app_context():
        loans = Loan.query.all()
        for loan in loans:
            penalty = apply_daily_penalty(loan)
            if penalty > 0:
                client = Client.query.get(loan.client_id)
                send_sms(client.phone, f"Loan overdue. New balance: {loan.balance}")
        db.session.commit()


scheduler.add_job(daily_jobs, 'interval', hours=24)
scheduler.start()





