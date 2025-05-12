from app import db
from app.models import FaseAtual, Ranking
from datetime import datetime
from flask import Blueprint, jsonify


def calcular_pontuacao(usuario_id):
    fases = FaseAtual.query.filter_by(usuario_id=usuario_id).all()
    total_pontos = 0
    tempo_total = 0

    for fase in fases:
        tempo_fase = (fase.horario_final_fase - fase.horario_inicio_fase).total_seconds()
        tempo_total += tempo_fase
        
        # Precisa colocar a pontuação aqui, conforme as respostas do usuário

    ranking = Ranking.query.filter_by(usuario_id=usuario_id).first()
    if ranking:
        ranking.pontos = total_pontos
        ranking.tempo_total = tempo_total
    else:
        ranking = Ranking(usuario_id=usuario_id, pontos=total_pontos, tempo_total=tempo_total)
        db.session.add(ranking)

    db.session.commit()

bp = Blueprint('ranking', __name__, url_prefix='/ranking')

@bp.route('/ranking_total', methods=['GET'])
def ranking_total():
    rankings = Ranking.query.order_by(Ranking.pontos.desc()).all()
    ranking_list = [
        {
            'usuario': ranking.usuario.nome,
            'pontos': ranking.pontos,
            'tempo_total': ranking.tempo_total
        }
        for ranking in rankings
    ]
    return jsonify(ranking_list), 200

