# Adicionei o carregamento das variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
import os

load_dotenv()

# Substitua as variáveis sensíveis por chamadas ao os.getenv
API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')