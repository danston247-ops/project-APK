
from flask import Blueprint, jsonify
from models import Client, Loan

mobile_bp = Blueprint('mobile', __name__, url_prefix='/api/mobile')

@mobile_bp.route('/clients')
def mobile_clients():
    clients = Client.query.all()
    return jsonify([{ "id": c.id, "name": c.name, "phone": c.phone } for c in clients])

@mobile_bp.route('/loans/<int:client_id>')
def mobile_loans(client_id):
    loans = Loan.query.filter_by(client_id=client_id).all()
    return jsonify([{ "balance": l.balance } for l in loans])