from dataclasses import dataclass
from datetime import datetime

@dataclass
class RegistroFinanceiro:
    tipo: str                   # "gasto" ou "ganho"
    descricao: str              # descrição ou origem
    valor: float                # valor numerico ex: 11.0
    pagamento: str or None      # forma que gastou ou vazio para ganhos
    data: datetime              # Modificado aqui para datetime