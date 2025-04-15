from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
from .parser import parse_message
from .sheets import registrar

app = FastAPI()

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Substitua pelos valores reais da sua conta Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/webhook", response_class=JSONResponse)
async def whatsapp_webhook(request: Request):
    form = await request.form()
    #print("Dados recebidos:", form)  # Log para depuração
    # Captura dados enviados pela requisição
    text = form.get("Body")  # Twilio envia a mensagem no campo 'Body'
    from_ = form.get("From")  # Número de onde a mensagem foi recebida

    if not text or not from_:
        return PlainTextResponse(content="Campos 'Body' ou 'From' faltando", status_code=400)

    try:
        # Processa a mensagem recebida
        registro = parse_message(text)
        print(f"Registro processado: {registro}")  # Log para depuração
        registrar(registro)
        registro_valor_str = f"{registro.valor:.2f}".replace('.', ',')
        mensagem_resposta = (
            f"Registro adicionado!\nTipo: {registro.tipo},\nDescrição: {registro.descricao},\n"
            f"Valor: R$ {registro_valor_str},\nMétodo: {registro.pagamento}"
        )

        # Envia resposta de confirmação de volta ao remetente
        client.messages.create(
            body=mensagem_resposta,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=from_
        )
        
        return {"status": "success", "mensagem": mensagem_resposta}

    except Exception as e:
        # Responde com erro específico
        erro_msg = f"Erro: {str(e)}"
        return PlainTextResponse(content=erro_msg, status_code=400)