from flask import Blueprint, request, jsonify
from app import db
from app.models import Tentativa, FaseAtual, Pergunta, Resposta

bp = Blueprint('tentativa', __name__, url_prefix='/tentativa')

# Criar tentativa
@bp.route('/', methods=['POST'])
def criar_tentativa():
    data = request.get_json()

    nova_tentativa = Tentativa(
        id_fase_atual=data['id_fase_atual'],
        id_pergunta=data['id_pergunta'],
        id_resposta=data['id_resposta'],
        correta=data['correta']
    )
    db.session.add(nova_tentativa)
    db.session.commit()

    return jsonify({'mensagem': 'Tentativa registrada com sucesso', 'tentativa': nova_tentativa.to_dict()}), 201

# Listar todas as tentativas
@bp.route('/all', methods=['GET'])
def listar_todas_tentativas():
    tentativas = Tentativa.query.all()
    return jsonify([t.to_dict() for t in tentativas]), 200

# Listar tentativas por fase atual
@bp.route('/fase_atual/<int:id_fase_atual>', methods=['GET'])
def listar_por_fase_atual(id_fase_atual):
    tentativas = Tentativa.query.filter_by(id_fase_atual=id_fase_atual).all()
    return jsonify([t.to_dict() for t in tentativas]), 200

# Listar tentativas por pergunta
@bp.route('/pergunta/<int:id_pergunta>', methods=['GET'])
def listar_por_pergunta(id_pergunta):
    tentativas = Tentativa.query.filter_by(id_pergunta=id_pergunta).all()
    return jsonify([t.to_dict() for t in tentativas]), 200

# Buscar tentativa específica
@bp.route('/<int:id>', methods=['GET'])
def buscar_tentativa(id):
    tentativa = Tentativa.query.get_or_404(id)
    return jsonify(tentativa.to_dict()), 200

# Deletar tentativa
@bp.route('/<int:id>', methods=['DELETE'])
def deletar_tentativa(id):
    tentativa = Tentativa.query.get_or_404(id)
    db.session.delete(tentativa)
    db.session.commit()
    return jsonify({'mensagem': f'Tentativa #{id} deletada com sucesso'}), 200
