from .models import RegistroFinanceiro
from .perplexity_ai import interpretar_mensagem_perplexity  # ou cole direto se preferir

def parse_message_ai(mensagem: str) -> RegistroFinanceiro:
    resultado = interpretar_mensagem_perplexity(mensagem)
    # Ajuste de proteção caso IA retorne campos não esperados
    tipo = resultado.get('tipo', 'outro')
    descricao = resultado.get('descricao', 'Não informado')
    valor = resultado.get('valor')
    pagamento = resultado.get('pagamento', None)
    from datetime import datetime

    return RegistroFinanceiro(
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        pagamento=pagamento,
        data=datetime.now()
    )