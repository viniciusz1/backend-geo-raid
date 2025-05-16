from flask import Blueprint, jsonify, request
from app import db
from app.models import Fase, FaseAtual
from datetime import datetime
from app.routes.ranking import calcular_pontuacao

bp = Blueprint('fases', __name__, url_prefix='/fase')

# Adicionar após os endpoints existentes no Blueprint bp (fases)

@bp.route('/', methods=['POST'])
def criar_fase():
    data = request.get_json()
    nome = data.get('nome')
    sequencia = data.get('sequencia')

    if not nome or sequencia is None:
        return jsonify({'erro': 'Nome e sequência são obrigatórios'}), 400

    if Fase.query.filter_by(sequencia=sequencia).first():
        return jsonify({'erro': 'Já existe uma fase com essa sequência'}), 400

    nova_fase = Fase(nome=nome, sequencia=sequencia)
    db.session.add(nova_fase)
    db.session.commit()

    return jsonify({'mensagem': f'Fase "{nome}" criada com sucesso'}), 201


@bp.route('/<int:fase_id>', methods=['PUT'])
def editar_fase(fase_id):
    fase = Fase.query.get(fase_id)
    if not fase:
        return jsonify({'erro': 'Fase não encontrada'}), 404

    data = request.get_json()
    nome = data.get('nome')
    sequencia = data.get('sequencia')

    if nome:
        fase.nome = nome
    if sequencia is not None:
        if Fase.query.filter(Fase.sequencia == sequencia, Fase.id != fase_id).first():
            return jsonify({'erro': 'Já existe outra fase com essa sequência'}), 400
        fase.sequencia = sequencia

    db.session.commit()
    return jsonify({'mensagem': f'Fase atualizada com sucesso'}), 200

@bp.route('/', methods=['GET'])
def listar_fases():
    fases = Fase.query.order_by(Fase.sequencia).all()

    lista_fases = [
        {
            'id': fase.id,
            'nome': fase.nome,
            'sequencia': fase.sequencia
        }
        for fase in fases
    ]
    return jsonify(lista_fases), 200

@bp.route('/<int:fase_id>', methods=['DELETE'])
def deletar_fase(fase_id):
    fase = Fase.query.get(fase_id)
    if not fase:
        return jsonify({'erro': 'Fase não encontrada'}), 404

    db.session.delete(fase)
    db.session.commit()
    return jsonify({'mensagem': f'Fase "{fase.nome}" deletada com sucesso'}), 200
