from app import db
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100), unique=True, index=True)

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