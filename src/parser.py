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
    metodos = ['cartão de crédito', 'cartão de débito', 'pix', 'dinheiro', 'swile']
    return next((m for m in metodos if m in mensagem.lower()), None)

def extrair_descricao(mensagem: str, tipo:str):
    doc = nlp(mensagem.lower())

    # Primeiro tentar achar descrição após palavras-chave ("na", "no", "em", "com", "de")
    palavras_chave_pos = ['na', 'no', 'em', 'com', 'de']
    for idx, token in enumerate(doc):
        if token.text in palavras_chave_pos:
            possivel_desc = []
            for t in doc[idx+1:]:
                if t.pos_ in ['NOUN', 'PROPN', 'ADJ']:
                    possivel_desc.append(t.text)
                else:
                    break
            if possivel_desc:
                return ' '.join(possivel_desc).strip()

    # Se não achar, tentar formato "{verbo} {descrição} por R$ valor"
    padrao_antes_do_valor = r"(?:compr[^\s]*|vend[^\s]*|pag[^\s]*|gast[^\s]*|ganh[^\s]*|receb[^\s]*)\s+(.*?)\s+por\s+(?:r\$|\d)"

    match = re.search(padrao_antes_do_valor, mensagem.lower())
    if match:
        descricao = match.group(1)
        doc_desc = nlp(descricao)
        # remove artigos e pronomes
        possivel_desc = [t.text for t in doc_desc if t.pos_ in ['NOUN', 'PROPN', 'ADJ']]
        if possivel_desc:
            return ' '.join(possivel_desc).strip()

    return "Não informado"


def parse_message(mensagem: str) -> RegistroFinanceiro:
    doc = nlp(mensagem.lower())

    tipo = identificar_tipo(mensagem, doc)
    valor = extrair_valor(mensagem)
    pagamento = extrair_metodo_pagamento(mensagem) if tipo == 'Saída' else None
    descricao = extrair_descricao(mensagem, tipo)

    return RegistroFinanceiro(
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        pagamento=pagamento,
        data=datetime.now()
    )