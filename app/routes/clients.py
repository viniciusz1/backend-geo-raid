from flask import jsonify, request
from app import db
from app.models import Client
from app.routes import bp
from app.auth import token_required

@bp.route('/clients', methods=['GET'])
@token_required
def get_clients(current_user):
    client_id = request.args.get('client_id')

    if client_id:
        try:
            client = Client.query.get_or_404(client_id)
            return jsonify(client.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        try:
            clients = Client.query.all()
            return jsonify([client.to_dict() for client in clients]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@bp.route('/clients', methods=['POST'])
@token_required
def create_client(current_user):
    try:
        data = request.get_json()

        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        if Client.query.filter_by(name=data['name']).first():
            return jsonify({'error', 'Name already registered'}), 400
        if Client.query.filter_by(email=data['email']).first():
            return jsonify({'error', 'Email already registered'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/clients/<int:id>', methods=['PUT'])
@token_required
def update_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Sucessfully to delete client'}), 200

    except Exception as e:
        return jsonify({'error', str(e)}), 500


@bp.route('/clients/<int:id>', methods=['DELETE'])
@token_required
def delete_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        data = request.get_json() or {}

        if 'name' not in data or 'email' not in data:
            return jsonify({'error', 'Name and email are required'}), 400

        if Client.query.filter_by(name=data['name']).first():
            return jsonify({'error', 'Name already exists'}), 400

        if Client.query.filter_by(email=data['email']).first():
            return jsonify({'error', 'Email already registered'}), 400

        client.name = data['name']
        client.email = data['email']
        db.session.delete()
        return jsonify(client.to_dict()), 200

    except Exception as e:
        return jsonify({'error', str(e)}), 500