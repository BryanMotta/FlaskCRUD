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


class disciplina_resource(Resource):
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

    @trc.default_trace('http:get:disciplina_resource')
    def get(self):
        response = disciplinas_schema.jsonify(Disciplina.query.all())
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        return response
        
    @trc.default_trace('http:get:disciplina_resource')
    def post(self):
        nova_disciplina = Disciplina(request.json['nome'])

        db.session.add(nova_disciplina)
        db.session.commit()

        response = disciplina_schema.jsonify(nova_disciplina)
        response.status_code = 201
        response.headers['Content-Type'] = 'application/json'
        return response

    @trc.default_trace('http:get:disciplina_resource')
    def delete(self):
        disciplina_id = request.json['disciplina_id']
        disciplina = Disciplina.query.get(disciplina_id)

        db.session.delete(disciplina)
        db.session.commit()

        response = Response()
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        return response

    @trc.default_trace('http:get:disciplina_resource')
    def put(self):

        disciplina_id = request.json['disciplina_id']
        disciplina_db = Disciplina.query.get(disciplina_id)
        disciplina_db.nome = request.json['nome']

        db.session.add(disciplina_db)
        db.session.commit()

        response = disciplina_schema.jsonify(disciplina_db)
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        return response