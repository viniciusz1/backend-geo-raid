from flask import Blueprint, request, jsonify
from app import db
from app.models import Pergunta, Fase

bp = Blueprint('pergunta', __name__, url_prefix='/pergunta')

# Criar pergunta
@bp.route('/', methods=['POST'])
def criar_pergunta():
    data = request.get_json()

    nova_pergunta = Pergunta(
        posicao_no_jogo=data['posicao_no_jogo'],
        descricao=data['descricao'],
        dificuldade=data['dificuldade'],
        pontuacao_acerto=data['pontuacao_acerto'],
        pontuacao_erro=data['pontuacao_erro'],
        id_fase=data['id_fase']
    )
    db.session.add(nova_pergunta)
    db.session.commit()

    return jsonify({'mensagem': 'Pergunta criada com sucesso', 'pergunta': nova_pergunta.to_dict()}), 201

# Listar todas as perguntas
@bp.route('/all', methods=['GET'])
def listar_todas_perguntas():
    perguntas = Pergunta.query.all()
    return jsonify([p.to_dict() for p in perguntas]), 200

# Buscar perguntas de uma fase
@bp.route('/fase/<int:id_fase>', methods=['GET'])
def listar_perguntas_por_fase(id_fase):
    perguntas = Pergunta.query.filter_by(id_fase=id_fase).all()
    return jsonify([p.to_dict() for p in perguntas]), 200

# Buscar uma pergunta específica
@bp.route('/<int:id>', methods=['GET'])
def buscar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    return jsonify(pergunta.to_dict()), 200

# Editar pergunta
@bp.route('/<int:id>', methods=['PUT'])
def editar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    data = request.get_json()

    pergunta.posicao_no_jogo = data.get('posicao_no_jogo', pergunta.posicao_no_jogo)
    pergunta.descricao = data.get('descricao', pergunta.descricao)
    pergunta.dificuldade = data.get('dificuldade', pergunta.dificuldade)
    pergunta.pontuacao_acerto = data.get('pontuacao_acerto', pergunta.pontuacao_acerto)
    pergunta.pontuacao_erro = data.get('pontuacao_erro', pergunta.pontuacao_erro)
    pergunta.id_fase = data.get('id_fase', pergunta.id_fase)

    db.session.commit()
    return jsonify({'mensagem': 'Pergunta atualizada com sucesso', 'pergunta': pergunta.to_dict()}), 200

# Deletar pergunta
@bp.route('/<int:id>', methods=['DELETE'])
def deletar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    db.session.delete(pergunta)
    db.session.commit()
    return jsonify({'mensagem': f'Pergunta #{id} deletada com sucesso'}), 200
