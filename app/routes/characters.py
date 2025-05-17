from flask import jsonify, request
from app import db
from app.models import Character
from app.routes import bp
from app.auth import token_required

@bp.route('/characters', methods=['GET'])
@token_required
def get_characters(current_character):
    character_id = request.args.get('character_id')

    if character_id:
        try:
            character = Character.query.get_or_404(character_id)
            return jsonify(character.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        try:
            characters = Character.query.all()
            return jsonify([character.to_dict() for character in characters]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@bp.route('/characters', methods=['POST'])
def create_character():
    try:
        data = request.get_json()

        if 'name' not in data or 'skin' not in data:
            return jsonify({'error': 'Name and Skin are required'}), 400
        if Character.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Name already registered'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    
    character = Character(name=data['name'], skin=data['skin'])
    db.session.add(character)
    db.session.commit()
    return jsonify(character.to_dict()), 201

@bp.route('/characters/<int:id>', methods=['PUT'])
@token_required
def update_character(current_character, id):
    try:
        data = request.get_json() or {}
        character = Character.query.get_or_404(id)

        if 'name' not in data or 'skin' not in data:
            return jsonify({'error': 'Name and Skin are required'}), 400

        # Optional: validate if name/skin already exists in other characters
        if Character.query.filter(Character.name == data['name'], Character.id != id).first():
            return jsonify({'error': 'Name already exists'}), 400
        if Character.query.filter(Character.skin == data['skin'], Character.id != id).first():
            return jsonify({'error': 'Skin already registered'}), 400

        character.name = data['name']
        character.skin = data['skin']
        db.session.commit()
        return jsonify(character.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/characters/<int:id>', methods=['DELETE'])
@token_required
def delete_character(current_character, id):
    try:
        character = Character.query.get_or_404(id)
        db.session.delete(character)
        db.session.commit()
        return jsonify({'message': 'Character deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
