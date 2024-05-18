import flask
import hashlib
from flask import request, render_template
import repository

PRIVATE_SALT="FIAP"
PRIVATE_HASH=hashlib.md5(PRIVATE_SALT.encode('UTF-8')).hexdigest()

SERVER_HOST = "localhost"
SERVER_PORT = 8080

app = flask.Flask(__name__)
print(__name__)
app.config["DEBUG"] = True

@app.route('/valida', methods=['GET'])
def valida():
    return render_template('valida.html')

@app.route('/token', methods=['GET'])
def token():
    return render_template('token.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/gerar-token', methods=['POST'])
def gerar_token():
    numero_cliente = request.form["numero_cliente"]
    numero_colaborador = request.form["numero_colaborador"]

    contact_salt = PRIVATE_HASH + numero_cliente + numero_colaborador
    contact_hash = hashlib.md5(contact_salt.encode('UTF-8'))
    
    repository.insert(contact_hash.hexdigest())
    return render_template('sucess.html')


@app.route('/validar-token', methods=['POST'])
def validar_token():
    meu_numero = request.form["meu_numero"]
    numero_suspeito = request.form["numero_suspeito"]

    test_salt = PRIVATE_HASH + meu_numero + numero_suspeito
    test_hash = hashlib.md5(test_salt.encode('UTF-8'))
    
    data = repository.get(test_hash.hexdigest())
    if data is None:
        return render_template('fail.html')
    return render_template('sucess.html')

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)