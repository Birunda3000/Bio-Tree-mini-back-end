'''from app import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)'''

def exibir():
    return print("----------------------------------------------Exibindo tags----------------------------------------------")