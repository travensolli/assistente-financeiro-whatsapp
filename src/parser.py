import spacy
from datetime import datetime
from price_parser import Price
from .models import RegistroFinanceiro
import re

nlp = spacy.load('pt_core_news_sm')

def extrair_valor(mensagem: str) -> float:
    preco = Price.fromstring(mensagem)
    if preco.amount is None:
        raise ValueError("Nenhum valor monetário claro encontrado.")
    return float(preco.amount)

def identificar_tipo(mensagem: str, doc) -> str:
    verbos_gasto = ["gastar", "gastei", "comprar", "comprei", "pagar", "paguei", "pago", "gastou", "comprou"]
    verbos_ganho = ["ganhar", "ganhei", "receber", "recebi", "vender", "vendi", "recebeu", "recebido", "ganhou", "vendeu"]

    for token in doc:
        texto = token.text.lower()
        lema = token.lemma_.lower()
        if texto in verbos_gasto or lema in verbos_gasto:
            return 'Saída'
        if texto in verbos_ganho or lema in verbos_ganho:
            return 'Entrada'

    raise ValueError("Não consegui classificar em ganho ou gasto.")

def extrair_metodo_pagamento(mensagem: str):
    metodos = {
        'cartão de crédito': 'Cartão de crédito',
        'cartao de crédito': 'Cartão de crédito',
        'cartao de credito': 'Cartão de crédito',
        'cartão de credito': 'Cartão de crédito',
        'cartão de débito': 'Cartão de débito',
        'cartao de débito': 'Cartão de débito',
        'cartao de debito': 'Cartão de débito',
        'cartão de debito': 'Cartão de débito',
        'pix': 'Pix',
        'dinheiro': 'Dinheiro',
        'swile': 'Swile',
        'vale': 'Vale',
        'saldo': 'Saldo'
    }
    for chave, valor in metodos.items():
        if chave in mensagem.lower():
            return valor
    return None

def extrair_descricao(mensagem: str, tipo: str):
    doc = nlp(mensagem.lower())

    # Padrão: verbo + descrição (até "com", "no", etc)
    padrao = r"(?:gastei|comprei|paguei|recebi|ganhei|vendi|comprou|gastou|pagou)[^\d]*?\d+[\.,]?\d*\s*(?:reais|r\$)?\s*(?:em|de|na|no|do|da)?\s*(.*?)(?:\s+(?:com|no|na|do|da|por|de|em)\s+.*)?$"
    match = re.search(padrao, mensagem.lower())
    if match:
        descricao_raw = match.group(1).strip()
        # Limpar palavras irrelevantes e formatar
        doc_desc = nlp(descricao_raw)
        palavras = [t.text for t in doc_desc if t.pos_ in ['NOUN', 'PROPN', 'ADJ'] and t.text.lower() not in ['reais', 'cartão', 'credito', 'cartao', 'pix', 'dinheiro', 'vale', 'saldo']]
        descricao = ' '.join(palavras).strip().capitalize()
        return descricao if descricao else "Não informado"

    return "Não informado"

def parse_message(mensagem: str) -> RegistroFinanceiro:
    doc = nlp(mensagem.lower())

    tipo = identificar_tipo(mensagem, doc)
    valor = extrair_valor(mensagem)
    pagamento = extrair_metodo_pagamento(mensagem) if tipo == 'Saída' else None
    if pagamento:
        pagamento = pagamento.strip().capitalize()
    descricao = extrair_descricao(mensagem, tipo)

    return RegistroFinanceiro(
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        pagamento=pagamento,
        data=datetime.now()
    )
