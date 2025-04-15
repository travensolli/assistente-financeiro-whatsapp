
from src.sheets import registrar
from src.models import RegistroFinanceiro
from datetime import datetime

registro_de_teste = RegistroFinanceiro(
    tipo="gasto",
    descricao="Teste integração planilha",
    valor=15.50,
    pagamento="Pix",
    data=datetime.now()
)

registrar(registro_de_teste)
print("✅ Registro teste adicionado com sucesso!")

# Rodar o comando abaixo para executar o teste:
# python -m tests.teste_sheets