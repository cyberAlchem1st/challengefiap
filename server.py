import hashlib
import os

import flask
from flask import request, render_template

import aes
import repository

SECRET = os.getenv("SECRET_KEY")

SERVER_HOST = "localhost"
SERVER_PORT = 8080

app = flask.Flask(__name__)
print(__name__)
app.config["DEBUG"] = True

aes_tool = aes.AESCipher(SECRET)
print('Encryption tool initialized\n')


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

    contact_salt = numero_cliente + numero_colaborador

    user_id = hashlib.md5(numero_cliente.encode('UTF-8')).hexdigest()
    secret = aes_tool.encrypt(contact_salt)

    repository.insert(user_id, secret.decode("utf-8"))
    return render_template('sucess.html')


@app.route('/validar-token', methods=['POST'])
def validar_token():
    meu_numero = request.form["meu_numero"]
    numero_suspeito = request.form["numero_suspeito"]

    user_id = hashlib.md5(meu_numero.encode('UTF-8')).hexdigest()
    data = repository.get(user_id)

    validation_value = meu_numero + numero_suspeito

    print(data)
    try:
        secret_dec = aes_tool.decrypt(data["secret"])
        if secret_dec == validation_value:
            return render_template('sucess.html')
    except TypeError:
        return render_template('fail.html')

    return render_template('fail.html')


if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
