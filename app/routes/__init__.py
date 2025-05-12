from flask import Blueprint

# o bp vai pegar a função do main de iniciar o server flask
bp = Blueprint('main', __name__)

#import e encapsula as rotas no init usando o blueprint
from app.routes import users
from app.routes import characters
from app.routes import fases
 
bp.register_blueprint(fases.bp)