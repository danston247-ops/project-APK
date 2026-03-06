from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))

class FieldManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    encrypted_data = db.Column(db.Text)
    field_manager_id = db.Column(db.Integer, db.ForeignKey('field_manager.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    principal = db.Column(db.Float)
    balance = db.Column(db.Float)
    monthly_penalty = db.Column(db.Float, default=0.20)
    daily_penalty = db.Column(db.Float, default=0.01)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)

class Repayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'))
    amount = db.Column(db.Float)
    date_paid = db.Column(db.DateTime, default=datetime.utcnow)