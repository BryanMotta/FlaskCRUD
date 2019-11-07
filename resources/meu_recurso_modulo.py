# ! /usr/bin/python
import json
from flask import Response
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
from excecoes.custom_exception import CustomException
import logging
import opentracing
import flask
import apm.tracer.tracers as trc


class MeuRecurso(Resource):
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

    @trc.default_trace('http:get:MeuRecurso')
    def get(self):
        response = Response(json.dumps({"sucesso": True}, ensure_ascii=False, allow_nan=False))
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        return response

    @trc.default_trace('http:get:MeuRecurso')
    def post(self):
        response = Response()
        response.status_code = 201
        response.headers['Content-Type'] = 'application/json'
        response.headers['Location'] = '123'
        return response