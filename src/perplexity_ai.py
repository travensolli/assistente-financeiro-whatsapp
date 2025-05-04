import os
import requests
import json
from dotenv import load_dotenv
from .models import RegistroFinanceiro_ai

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def interpretar_mensagem_perplexity(mensagem):
    prompt = (
        "Você é um assistente financeiro. Leia a mensagem abaixo e retorne um JSON com os seguintes campos: "
        "tipo (Entrada ou Saída), "
        "valor (em float, se houver, senão None), "
        "descricao (apenas o descritivo curto do gasto ou ganho, ou None), "
        "pagamento (modalidade de pagamento: pix, dinheiro, cartão de débito, cartão de crédito, vale, swile, ou None). "
        "Mensagem: " + mensagem + ". "
        "Apenas retorne o JSON exato, sem texto adicional, explicações ou comentários."
    )

    api_key = os.getenv("PERPLEXITY_API_KEY")
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar",  # ou 'gpt-4', 'claude-3-sonnet', etc — veja o menu docs da perplexity
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um assistente financeiro que recebe mensagens em português."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": {
		    "type": "json_schema",
            "json_schema": {"schema": RegistroFinanceiro_ai.model_json_schema()},
        },
        "temperature": 0.0,
        "max_tokens": 256
    }

    response = requests.post(url, headers=headers, json=data).json()
    # Retorna somente o que está na resposta
    try:
        text = response['choices'][0]['message']['content']
        result = json.loads(text.strip())
        return result
    except Exception as e:
        print("Erro no parsing da resposta da API Perplexity:", e)
        print("Conteúdo retornado:", response.text)
        return {}
