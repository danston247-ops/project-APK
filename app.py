from flask import Flask, render_template, request, redirect, session, jsonify
from config import Config
from models import db, Admin, Client, Loan, Repayment, FieldManager
from utils import encrypt_data, mtn_request_to_pay, airtel_request_to_pay
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from mobile_api import mobile_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(mobile_bp)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Admin.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['admin'] = user.id
            return redirect('/admin')
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    total_clients = Client.query.count()
    loans = Loan.query.all()
    return render_template('admin_dashboard.html', total_clients=total_clients, loans=loans)

@app.route('/pay/mtn', methods=['POST'])
def pay_mtn():
    phone = request.form['phone']
    amount = request.form['amount']
    return jsonify(mtn_request_to_pay(phone, amount))

@app.route('/pay/airtel', methods=['POST'])
def pay_airtel():
    phone = request.form['phone']
    amount = request.form['amount']
    return jsonify(airtel_request_to_pay(phone, amount))

# ===== SMS =====
def send_sms(phone, message):
    if not Config.SMS_ENABLED:
        print(f"SMS disabled → {phone}: {message}")
        return

    from twilio.rest import Client as TwilioClient
    client = TwilioClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_=Config.TWILIO_PHONE, to=phone)

if __name__ == '__main__':
    from scheduler import scheduler  # start jobs
    app.run(host='0.0.0.0', port=5000, debug=True)