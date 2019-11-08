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


class turma_resource(Resource):
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

    @trc.default_trace('http:get:turma_resource')
    def get(self):
        response = turmas_schema.jsonify(Turma.query.all())
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        return response

    @trc.default_trace('http:get:turma_resource')
    def post(self):
        nome = request.json['nome']

        nova_turma = Turma(nome)

        db.session.add(nova_turma)
        db.session.commit()

        response = turma_schema.jsonify(nova_turma)
        response.status_code = 201
        response.headers['Content-Type'] = 'application/json'
        response.headers['Location'] = '123'
        return response

    @trc.default_trace('http:get:turma_resource')
    def delete(self):
        turma_id = request.json['turma_id']
        turma = Turma.query.get(turma_id)

        db.session.delete(turma)
        db.session.commit()

        return ''

    @trc.default_trace('http:get:turma_resource')
    def put(self):
        turma_id = request.json['turma_id']

        turma_db = Turma.query.get(turma_id)

        turma_db.nome = request.json['nome']

        db.session.add(turma_db)
        db.session.commit()

        return turma_schema.jsonify(turma_db)
