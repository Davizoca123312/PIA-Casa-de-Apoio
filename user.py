from flask_sqlalchemy import SQLAlchemy

# Inicializando o banco de dados
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    estado_civil = db.Column(db.String(50), nullable=False)

    medicamentos = db.relationship('Medicamento', backref='user', lazy=True)
    sobre_info = db.relationship('Sobre', backref='user', lazy=True)
    cids = db.relationship('Cid', backref='user', lazy=True)  # Relacionamento com CID

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    periodo = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Sobre(db.Model):
    __tablename__ = 'sobre'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# Nova tabela CID para armazenar os códigos CID dos pacientes
class Cid(db.Model):
    __tablename__ = 'cids'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False)  # Código CID (ex: F32)
    descricao = db.Column(db.String(255), nullable=False)  # Descrição do CID (ex: Depressão maior)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

