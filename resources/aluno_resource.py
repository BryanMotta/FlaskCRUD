# ! /usr/bin/python
import json
from flask import Response, request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
from excecoes.custom_exception import CustomException
import logging
import opentracing
import flask
import apm.tracer.tracers as trc
from models import *


class aluno_resource(Resource):
    """
    MeuRecurso: Recurso executar opreacao <operacao a descrever>

    Para testar o GET executar

    .. code-block:: bash
       :linenos:

       curl -X GET -H "Cache-Control: no-cache" "http://localhost:8000/template_api/resource_path"

    Deve retornar

    .. code-block:: javascript
       :linenos:

       {
          "sucesso": true
        }

    Para testar o POST executar

    .. code-block:: bash
       :linenos:

        curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{
        "teste": "123"
        }' "http://localhost:8000/template_api/resource_path"
        
    """

    @trc.default_trace('http:get:aluno_resource')
    def get(self):
        response = Response(json.dumps(Aluno.query.all()))
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        return response

    @trc.default_trace('http:get:aluno_resource')
    def post(self):   
        disciplina_id = request.json['disciplina_id']

        novo_aluno = Aluno(
            request.json['nome'],
            request.json['cpf'],
            request.json['turma_id']
        )

        disciplina = Disciplina.query.get(disciplina_id)
        disciplina.alunos.append(novo_aluno)

        db.session.add(novo_aluno)
        db.session.commit()

        return aluno_schema.jsonify(novo_aluno)

    @trc.default_trace('http:get:aluno_resource')
    def delete(self):
        aluno_id = request.json['aluno_id']
        aluno = Aluno.query.get(aluno_id)

        db.session.delete(aluno)
        db.session.commit()

        return ''


    @trc.default_trace('http:get:aluno_resource')
    def put(self):

        aluno_id = request.json['aluno_id']

        aluno_db = Aluno.query.get(aluno_id)

        aluno_db.nome = request.json['nome']
        aluno_db.cpf = request.json['cpf']
        aluno_db.turma_id = request.json['turma_id']

        db.session.add(aluno_db)
        db.session.commit()

        return aluno_schema.jsonify(aluno_db) 




