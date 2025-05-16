from flask import Blueprint, jsonify, request
from app import db
from app.models import Fase, FaseAtual
from datetime import datetime
from app.routes.ranking import calcular_pontuacao

bp = Blueprint('fase_atual', __name__, url_prefix='/fase_atual')

@bp.route('/', methods=['GET'])
def buscar_fase_atual():
    fase_atual = FaseAtual.query.order_by(FaseAtual.id.desc()).first()

    if not fase_atual:
        return jsonify({'erro': 'Nenhuma fase atual encontrada'}), 404

    dados = {
        'id': fase_atual.id,
        'fase_id': fase_atual.fase_id,
        'fase_nome': fase_atual.fase.nome,
        'sequencia': fase_atual.fase.sequencia,
        'horario_inicio_fase': fase_atual.horario_inicio_fase.isoformat() if fase_atual.horario_inicio_fase else None,
        'horario_final_fase': fase_atual.horario_final_fase.isoformat() if fase_atual.horario_final_fase else None,
        'passou_fase': fase_atual.passou_fase
    }

    return jsonify(dados), 200



@bp.route('/iniciar', methods=['POST'])
def iniciar_fase():
    ultima_fase_atual = FaseAtual.query.order_by(FaseAtual.id.desc()).first()

    if ultima_fase_atual:
        ultima_sequencia = ultima_fase_atual.fase.sequencia
    else:
        ultima_sequencia = 0

    proxima_fase = Fase.query.filter(Fase.sequencia > ultima_sequencia).order_by(Fase.sequencia).first()

    if not proxima_fase:
        return jsonify({'erro': 'Nenhuma próxima fase disponível'}), 400

    nova_fase_atual = FaseAtual(
        fase_id=proxima_fase.id,
        horario_inicio_fase=datetime.utcnow()
    )
    db.session.add(nova_fase_atual)
    db.session.commit()

    return jsonify({'mensagem': f'Fase {proxima_fase.nome} iniciada com sucesso'}), 201


@bp.route('/finalizar/<int:fase_atual_id>', methods=['POST'])
def finalizar_fase(fase_atual_id):
    fase_atual = FaseAtual.query.get(fase_atual_id)

    if not fase_atual:
        return jsonify({'erro': 'FaseAtual não encontrada'}), 404

    fase_atual.horario_final_fase = datetime.utcnow()
    fase_atual.passou_fase = True

    db.session.commit()

    calcular_pontuacao(fase_atual.usuario_id)

    return jsonify({'mensagem': f'Fase {fase_atual.fase.nome} finalizada com sucesso'}), 200
