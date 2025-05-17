from flask import Blueprint

# o bp vai pegar a função do main de iniciar o server flask
bp = Blueprint('main', __name__)

#import e encapsula as rotas no init usando o blueprint
from app.routes import users
from app.routes import characters
from app.routes import fase
from app.routes import fase_atual
from app.routes import ranking
from app.routes import pergunta
from app.routes import resposta

bp.register_blueprint(fase.bp)
bp.register_blueprint(ranking.bp)
bp.register_blueprint(fase_atual.bp)
bp.register_blueprint(pergunta.bp)
bp.register_blueprint(resposta.bp)
