from flask import Blueprint, request, jsonify
from app import db
from app.models import Resposta, Pergunta

bp = Blueprint('resposta', __name__, url_prefix='/resposta')

# Criar resposta
@bp.route('/', methods=['POST'])
def criar_resposta():
    data = request.get_json()

    nova_resposta = Resposta(
        correta=data['correta'],
        descricao=data['descricao'],
        id_pergunta=data['id_pergunta']
    )
    db.session.add(nova_resposta)
    db.session.commit()

    return jsonify({'mensagem': 'Resposta criada com sucesso', 'resposta': nova_resposta.to_dict()}), 201

# Listar todas as respostas
@bp.route('/all', methods=['GET'])
def listar_todas_respostas():
    respostas = Resposta.query.all()
    return jsonify([r.to_dict() for r in respostas]), 200

# Listar respostas de uma pergunta
@bp.route('/pergunta/<int:id_pergunta>', methods=['GET'])
def listar_respostas_por_pergunta(id_pergunta):
    respostas = Resposta.query.filter_by(id_pergunta=id_pergunta).all()
    return jsonify([r.to_dict() for r in respostas]), 200

# Buscar uma resposta específica
@bp.route('/<int:id>', methods=['GET'])
def buscar_resposta(id):
    resposta = Resposta.query.get_or_404(id)
    return jsonify(resposta.to_dict()), 200

# Editar resposta
@bp.route('/<int:id>', methods=['PUT'])
def editar_resposta(id):
    resposta = Resposta.query.get_or_404(id)
    data = request.get_json()

    resposta.correta = data.get('correta', resposta.correta)
    resposta.descricao = data.get('descricao', resposta.descricao)
    resposta.id_pergunta = data.get('id_pergunta', resposta.id_pergunta)

    db.session.commit()
    return jsonify({'mensagem': 'Resposta atualizada com sucesso', 'resposta': resposta.to_dict()}), 200

# Deletar resposta
@bp.route('/<int:id>', methods=['DELETE'])
def deletar_resposta(id):
    resposta = Resposta.query.get_or_404(id)
    db.session.delete(resposta)
    db.session.commit()
    return jsonify({'mensagem': f'Resposta #{id} deletada com sucesso'}), 200
