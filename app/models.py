from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(1000), index=True)

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True, unique=True)
    character = db.relationship('Character', back_populates='user', uselist=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'character_id': self.character_id,
        }
        if self.character:
            data['character'] = {
                'id': self.character.id,
                'name': self.character.name,
                'skin': self.character.skin,
            }
        return data
    
class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    skin = db.Column(db.String(100), unique=True, index=True)

    user = db.relationship('Usuario', back_populates='character', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'skin': self.skin
        }

class Fase(db.Model):
    __tablename__ = 'fase'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sequencia = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self):
        return f"<Fase {self.nome} (Sequência {self.sequencia})>"
    
class Pergunta(db.Model):
    __tablename__ = 'pergunta'

    id = db.Column(db.Integer, primary_key=True)
    posicao_no_jogo = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    dificuldade = db.Column(db.String(50), nullable=False)
    pontuacao_acerto = db.Column(db.Integer, nullable=False)
    pontuacao_erro = db.Column(db.Integer, nullable=False)

    id_fase = db.Column(db.Integer, db.ForeignKey('fase.id'), nullable=False)
    fase = db.relationship('Fase', backref='perguntas')

    def to_dict(self):
        return {
            'id': self.id,
            'posicao_no_jogo': self.posicao_no_jogo,
            'descricao': self.descricao,
            'dificuldade': self.dificuldade,
            'pontuacao_acerto': self.pontuacao_acerto,
            'pontuacao_erro': self.pontuacao_erro,
            'id_fase': self.id_fase
        }


class Resposta(db.Model):
    __tablename__ = 'resposta'

    id = db.Column(db.Integer, primary_key=True)
    correta = db.Column(db.Boolean, nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    
    id_pergunta = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)
    pergunta = db.relationship('Pergunta', backref='respostas')

    def to_dict(self):
        return {
            'id': self.id,
            'correta': self.correta,
            'descricao': self.descricao,
            'id_pergunta': self.id_pergunta
        }

class Tentativa(db.Model):
    __tablename__ = 'tentativa'

    id = db.Column(db.Integer, primary_key=True)
    id_fase_atual = db.Column(db.Integer, db.ForeignKey('fase_atual.id'), nullable=False)
    id_pergunta = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)
    id_resposta = db.Column(db.Integer, db.ForeignKey('resposta.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    horario = db.Column(db.DateTime, default=datetime.utcnow)
    correta = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'id_fase_atual': self.id_fase_atual,
            'id_pergunta': self.id_pergunta,
            'id_resposta': self.id_resposta,
            'id_usuario': self.id_usuario,
            'horario': self.horario.isoformat(),
            'correta': self.correta
        }


class FaseAtual(db.Model):
    __tablename__ = 'fase_atual'

    id = db.Column(db.Integer, primary_key=True)
    fase_id = db.Column(db.Integer, db.ForeignKey('fase.id'), nullable=False)
    horario_inicio_fase = db.Column(db.DateTime, nullable=True)
    horario_final_fase = db.Column(db.DateTime, nullable=True)
    passou_fase = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    fase = db.relationship('Fase')

    def __repr__(self):
        return f"<FaseAtual (Fase ID {self.fase_id})>"
    
class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) 
    pontos = db.Column(db.Integer, nullable=False)
    tempo_total = db.Column(db.Float, nullable=False)
    usuario = db.relationship('Usuario', backref='ranking', lazy=True) 
    def __repr__(self):
        return f'<Ranking {self.usuario.username} - {self.pontos} pontos>'
