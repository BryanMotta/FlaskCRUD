from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

alunos_disciplinas = db.Table('alunos_disciplinas', 
    db.Column('aluno_id', db.ForeignKey('aluno.aluno_id')),
    db.Column('disciplina_id', db.ForeignKey('disciplina.disciplina_id'))
)


# ALUNO MODEL ---------------------------------------------------------------------
class Aluno(db.Model):
    aluno_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    cpf = db.Column(db.String(11))
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.turma_id'))
    disciplinas = db.relationship('Disciplina', secondary=alunos_disciplinas, backref=db.backref('alunos'), lazy='dynamic')

    def __init__(self, nome, cpf, turma_id):
        self.nome = nome
        self.cpf = cpf
        self.turma_id = turma_id


class AlunoSchema(ma.Schema):
    class Meta:
        fields = ('aluno_id', 'nome', 'cpf', 'turma_id')


aluno_schema = AlunoSchema()
alunos_schema = AlunoSchema(many=True)


# DISCIPLINA MODEL ---------------------------------------------------------------------
class Disciplina(db.Model):
    disciplina_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))

    def __init__(self, nome):
        self.nome = nome


class DisciplinaSchema(ma.Schema):
    class Meta:
        fields = ('disciplina_id', 'nome')


disciplina_schema = DisciplinaSchema()
disciplinas_schema = DisciplinaSchema(many=True)


# TURMA MODEL ---------------------------------------------------------------------
class Turma(db.Model):
    turma_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    alunos = db.relationship('Aluno', backref='aluno')

    def __init__(self, nome):
        self.nome = nome


class TurmaSchema(ma.Schema):
    class Meta:
        fields = ('turma_id', 'nome')


turma_schema = TurmaSchema()
turmas_schema = TurmaSchema(many=True)