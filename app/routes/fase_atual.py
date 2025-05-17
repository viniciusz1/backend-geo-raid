from flask import Blueprint, jsonify, request
from app import db
from app.models import Fase, FaseAtual, Usuario
from datetime import datetime
from app.routes.ranking import calcular_pontuacao
from app.auth import token_required

bp = Blueprint('fase_atual', __name__, url_prefix='/fase_atual')




@bp.route('/', methods=['GET'])
@token_required
def buscar_fase_atual(current_user):
    fase_atual = FaseAtual.query \
        .filter_by(usuario_id=current_user.id) \
        .order_by(FaseAtual.id.desc()) \
        .first()

    if not fase_atual:
        return jsonify({'erro': 'Nenhuma fase atual encontrada para este usuário'}), 404

    dados = {
        'id': fase_atual.id,
        'fase_id': fase_atual.fase_id,
        'horario_inicio_fase': fase_atual.horario_inicio_fase.isoformat() if fase_atual.horario_inicio_fase else None,
        'horario_final_fase': fase_atual.horario_final_fase.isoformat() if fase_atual.horario_final_fase else None,
        'passou_fase': fase_atual.passou_fase,
        'passou_fase': fase_atual.usuario_id
    }

    return jsonify(dados), 200


@bp.route('/iniciar', methods=['POST'])
@token_required
def iniciar_fase(current_user):
    
    if isinstance(current_user, str): 
        current_user = Usuario.query.filter_by(username=current_user).first_or_404()

    fase_ativa = FaseAtual.query.filter_by(
        usuario_id=current_user.id,
        passou_fase=False
    ).filter(
        FaseAtual.horario_inicio_fase.isnot(None),
        FaseAtual.horario_final_fase.is_(None)
    ).first()

    if fase_ativa:
        return jsonify({
            'erro': 'Você já possui uma fase em andamento. Finalize a fase atual antes de iniciar uma nova.'
        }), 400

    ultima_fase_atual = FaseAtual.query \
        .filter_by(usuario_id=current_user.id) \
        .order_by(FaseAtual.id.desc()) \
        .first()

    if ultima_fase_atual:
        ultima_sequencia = ultima_fase_atual.fase.sequencia
    else:
        ultima_sequencia = 0

    proxima_fase = Fase.query \
        .filter(Fase.sequencia > ultima_sequencia) \
        .order_by(Fase.sequencia) \
        .first()

    if not proxima_fase:
        return jsonify({'erro': 'Nenhuma próxima fase disponível'}), 400

    # Cria o novo registro de FaseAtual
    nova_fase_atual = FaseAtual(
        fase_id=proxima_fase.id,
        usuario_id=current_user.id,
        horario_inicio_fase=datetime.utcnow()
    )
    db.session.add(nova_fase_atual)
    db.session.commit()

    return jsonify({'mensagem': f'Fase {proxima_fase.nome} iniciada com sucesso'}), 201



@bp.route('/finalizar', methods=['POST'])
@token_required
def finalizar_fase_ativa(current_user):
    
    if isinstance(current_user, str): 
        current_user = Usuario.query.filter_by(username=current_user).first_or_404()

    fase_atual = FaseAtual.query.filter_by(
        usuario_id=current_user.id,
        passou_fase=False
    ).filter(
        FaseAtual.horario_inicio_fase.isnot(None),
        FaseAtual.horario_final_fase.is_(None)
    ).first()

    if not fase_atual:
        return jsonify({'erro': 'Nenhuma fase ativa em andamento para este usuário.'}), 404

    fase_atual.horario_final_fase = datetime.utcnow()
    fase_atual.passou_fase = True

    db.session.commit()

    calcular_pontuacao(current_user.id)

    return jsonify({'mensagem': f'Fase {fase_atual.fase.nome} finalizada com sucesso.'}), 200


@bp.route('/<int:fase_atual_id>', methods=['DELETE'])
@token_required
def deletar_fase_atual(current_user, fase_atual_id):
    fase_atual = FaseAtual.query.get(fase_atual_id)

    if not fase_atual:
        return jsonify({'erro': 'FaseAtual não encontrada'}), 404

    db.session.delete(fase_atual)
    db.session.commit()

    return jsonify({'mensagem': f'Fase atual #{fase_atual.id} deletada com sucesso.'}), 200


@bp.route('/all', methods=['GET'])
def listar_todas_fases():
    fases = FaseAtual.query.all()

    lista_fases = [
        {
            'id': fase.id,
            'fase_id': fase.fase_id,
            'horario_inicio_fase': fase.horario_inicio_fase,
            'horario_final_fase': fase.horario_final_fase,
            'passou_fase': fase.passou_fase,
            'usuario_id': fase.usuario_id,
        }
        for fase in fases
    ]
    return jsonify(lista_fases), 200