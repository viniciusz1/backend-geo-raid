from flask import Blueprint, jsonify, request
from app import db
from app.models import Fase, FaseAtual
from datetime import datetime

bp = Blueprint('fases', __name__, url_prefix='/fase')

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

    return jsonify({'mensagem': f'Fase {fase_atual.fase.nome} finalizada com sucesso'}), 200
