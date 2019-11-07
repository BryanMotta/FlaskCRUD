#! /usr/bin/python python3
from flask import Flask, jsonify
from werkzeug.wrappers import Response
from flask_restful import Api
from excecoes.custom_exception import CustomException
import uuid
import logging
from recurso.status import Status
import json
from resources.meu_recurso_modulo import MeuRecurso
from datetime import datetime
import apm.tracer.tracer_config as trc_config
import apm.tracer.tracers as trc
from monitoring import setup
from monitoring.resource import Metrics
from models import *
import os


app = Flask(__name__)
api = Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSON_AS_ASCII'] = False
token = {'token': str(uuid.uuid4())}
start_time = datetime.now()
setup.setup_metrics(app)
api.add_resource(Metrics, '/template_api/metrics')
api.add_resource(MeuRecurso, '/template_api/resource_path')
api.add_resource(Status, '/template_api/status',
                 resource_class_kwargs={'configuracoes': token,
                                        'start_time': start_time}
                 )

trc_config.init_tracer("template_api")
logger = logging.getLogger(__name__)

DB_HOST = os.environ['DB_HOSTS']

app.config['SQLALCHEMY_DATABASE_URI'] = DB_HOST
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
ma.init_app(app)
db.create_all()

@app.errorhandler(Exception)
@trc.default_trace('exception:default_exception')
def default_error_handler(error):
    logger.exception('mensagem={}'.format(error).replace('\n', ' '))
    response = Response(json.dumps({'codigo': -100,'mensagem': 'Erro interno. Entrar em contato com a Ipiranga.'}, ensure_ascii=False))
    response.status_code = 500
    response.headers = {'Content-Type': 'application/json'}
    logger.info('http_status={} mensagem={}'.format(response.status_code, response.get_data()))
    return response


@app.errorhandler(CustomException)
@trc.default_trace('exception:custom_exception')
def custom_error_handler(error):
    response = Response(json.dumps(error.to_dict(), ensure_ascii=False))
    response.status_code = error.status_code
    response.headers = {'Content-Type': 'application/json'}
    if error.headers:
        for header, value in error.headers.items():
            response.headers[header] = value

    logger.info('http_status={} mensagem={}'.format(response.status_code, response.get_data().decode('utf8')))
    return response

if __name__ == '__main__':
    logger.info('Iniciando servico')
    app.run('0.0.0.0', 8080)