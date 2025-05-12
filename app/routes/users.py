from flask import jsonify, request
from app import db
from app.models import Character, Usuario
from app.routes import bp
from app.auth import token_required

@bp.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    user_id = request.args.get("user_id")

    if user_id:
        try:
            usuario = Usuario.query.get_or_404(user_id)
            return jsonify(usuario.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        try:
            users = Usuario.query.all()
            return jsonify([usuario.to_dict() for usuario in users]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()

        if "username" not in data or "password" not in data:
            return jsonify({"error": "Name and email are required"}), 400
        if Usuario.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Name already registered"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    user = Usuario(username=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@bp.route("/users/<int:id>", methods=["PUT"])
@token_required
def update_user(current_user, id):
    try:
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Sucessfully to delete usuario"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/users/<int:id>", methods=["DELETE"])
@token_required
def delete_user(current_user, id):
    try:
        usuario = Usuario.query.get_or_404(id)
        data = request.get_json() or {}

        if "name" not in data or "email" not in data:
            return jsonify({"error": "Name and email are required"}), 400

        if Usuario.query.filter_by(name=data["name"]).first():
            return jsonify({"error": "Name already exists"}), 400

        if Usuario.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 400

        usuario.name = data["name"]
        usuario.email = data["email"]
        db.session.delete()
        return jsonify(usuario.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/users/<int:user_id>/character", methods=["POST"])
@token_required
def select_character(current_user, user_id):
    data = request.get_json() or {}

    character_id = data.get("character_id")
    if not character_id:
        return jsonify({"error": "character_id é obrigatório"}), 400
    usuario = Usuario.query.get_or_404(user_id)
    character = Character.query.get_or_404(character_id)
    if usuario.character:
        return jsonify({"error": "Usuário já possui um personagem"}), 400
    usuario.character = character
    db.session.commit()
    return jsonify(usuario.to_dict()), 200


@bp.route("/users/<int:id>/character", methods=["PUT"])
@token_required
def update_character_link(current_user, id):
    data = request.get_json() or {}

    character_id = data.get("character_id")
    if not character_id:
        return jsonify({"error": "character_id é obrigatório"}), 400
    usuario = Usuario.query.get_or_404(id)
    character = Character.query.get_or_404(character_id)
    
    if usuario.character.id == character.id:
        return jsonify({"error": "Usuário já possui esse personagem"}), 400
    
    usuario.character = character
    db.session.commit()
    return jsonify(usuario.to_dict()), 200
