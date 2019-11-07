## Como utilizar o template

### 1. Criar documentacao

```bash
pip install Sphinx
cd flask_template
sphinx-apidoc . -o docs/source --force
make -C docs html
```

### 2. Libs usadas

Para incluir novos recursos Rest verificar a api [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/)