#Esse arquivo será usado para conectar e escrever dados diretamente no google sheets
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .models import RegistroFinanceiro
from dotenv import load_dotenv

load_dotenv()

# Checagem única: se não existe o arquivo de credenciais, cria a partir do env
if not os.path.exists('credentials.json'):
    creds_content = os.environ.get('GOOGLE_CREDS_JSON')
    if not creds_content:
        raise RuntimeError("Variável de ambiente GOOGLE_CREDS_JSON não definida!")
    with open('credentials.json', 'w') as f:
        f.write(creds_content)


def registrar(registro: RegistroFinanceiro):
    # Definição do escopo da API para o Google Sheets e autenticação
    scope = ["https://spreadsheets.google.com/feeds", 
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Abre planilha pelo nome (Altere para o nome exato da SUA planilha criada)
    sheet = client.open("Controle Financeiro Whatsapp").worksheet("Registros")
    print("Planilha aberta com sucesso!")
    # Adiciona uma nova linha no fim da planilha
    linha = [
        registro.data.isoformat(), # Data no formato ISO (AAAA-MM-DD) 
        registro.tipo.capitalize(), #Ganho ou Gasto com letra inicial em maiúscula
        registro.descricao.capitalize(),
        registro.valor,
        registro.pagamento if registro.pagamento else "" # pagamento "-" se vazio (ganho)
    ]

    sheet.append_row(linha)