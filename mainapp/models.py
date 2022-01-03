from mainapp import db
from datetime import datetime


class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    relacao = db.relationship('PassStorer', backref='senhas', lazy=True)

    def __repr__(self):
        return f'{self.password}'

class PassStorer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senha_id = db.Column(db.Integer, db.ForeignKey('passwords.id'), nullable=False)
    nome = db.Column(db.String(60), nullable=False)
    tempo = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    
    def __repr__(self):
        return f'{self.nome}'