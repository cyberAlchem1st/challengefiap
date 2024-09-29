import os
import telebot
import requests

SECRET = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(SECRET)
VALIDATION_URL = "http://localhost:8080/validar-token"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, """
    Bem vindo ao autoatendimento das lojas Maisbarato!
    Por favor, selecione uma opção:
    1 - Validar atendimento
    2 - Emitir segunda via
    3 - Rastrear entrega
    4 - Outros
    """)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    if("1" in message.text):
        sent = bot.reply_to(message, """
        Tudo bem, vamos precisar do seu numero para continuar!
        Informe no seguinte formato: (11) 91234-1234:
        """)
        bot.register_next_step_handler(sent, customer_number)

def customer_number(message):
    _customer_number = message.text
    sent = bot.reply_to(message, f"""
        Seu numero é {_customer_number}?
        Responda S para "SIM" e N para "NÃO"
        """)
    bot.register_next_step_handler(sent, customer_number_confirmation, _customer_number)


def customer_number_confirmation(message, _customer_number):
    answer = message.text
    if("S" in answer):
        sent = bot.reply_to(message, """
        Obrigado! Agora informe o número do atendente que entrou em contato
        Informe no seguinte formato: (11) 91234-1234:
        """)
        bot.register_next_step_handler(sent, provider_number, _customer_number)
    else:
        sent = bot.reply_to(message, """
        Tudo bem! Informe o número novamente ;)
        Informe no seguinte formato: (11) 91234-1234:
        """)
        bot.register_next_step_handler(sent, customer_number)

def provider_number_confirmation(message, _customer_number, _provider_number):
    answer = message.text
    if("S" in answer):
        sent = bot.reply_to(message, """
        Obrigado, aguarde enquanto validamos o atendimento!
        """)
        validation(sent, _customer_number, _provider_number)
    else:
        sent = bot.reply_to(message, """
        Tudo bem! Informe o número novamente ;)
        Informe no seguinte formato: (11) 91234-1234:
        """)
        bot.register_next_step_handler(sent, provider_number)

def provider_number(message, _customer_number):
    _provider_number = message.text

    sent = bot.reply_to(message, f"""
        O número do atendente é {_provider_number}?
        Responda S para "SIM" e N para "NÃO"
        """)
    bot.register_next_step_handler(sent, provider_number_confirmation, _customer_number, _provider_number)

def validation(message, _customer_number, _provider_number):
    _provider = _provider_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    _customer = _customer_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")

    payload = {"meu_numero": _customer, "numero_suspeito": _provider}
    x = requests.post(VALIDATION_URL, payload)

    if(x.status_code == 200):
        bot.reply_to(message, "Verificamos aqui e o atendidmento é valido e confiável ;D")

    else:
        bot.reply_to(message, """
        Não conseguimos vaidar o atendimento!
        Por motivos de segurança não mantenha contato com o número informado!
        """)

bot.infinity_polling()