# ! /usr/bin/python
import unittest
import os
os.environ['WITH_TRACER']='true'
os.environ['TRACER_HOST']='localhost'
os.environ['TRACER_PORT']='5775'
os.environ['TRACER_TOKEN']='123'
os.environ['FLASK_SUPPORT']='true'
os.environ['TOKEN']='123'
os.environ['SERVICE_NAME']='template_api'
from mock import patch
import json
from main import app


class MeuRecursoTest(unittest.TestCase):

    """
    Efetua todos os testes de comportamento do recurso
    """
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_get_meu_recurso_modulo_path(self):
        """
        Testa o metodo get <descrever cenario>
        """
        response = self.app.get('/template_api/resource_path?token=%s' % '123',
                                 follow_redirects=True
                                 )
        self.assertEqual(response.status_code, 200)

    def test_post_meu_recurso_modulo_path(self):
        """
        Testa o metodo post <descrever cenario>
        """
        response = self.app.post('/template_api/resource_path?token=%s' % '123',
                                 follow_redirects=True
                                 )
        self.assertEqual(response.status_code, 201)