from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100), unique=True, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
    
class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, index=True)
    skin = db.Column(db.String(100), unique=True, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'skin': self.skin
        }