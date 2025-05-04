from src.ai_parser import parse_message_ai

testes = [
    "Gastei R$1100,45 na padaria com cartão de crédito",
    "Ganhei R$ 3.250,00 de salario",
    "Recebi 1500 reais de presente",
    "Gastei R$ 1.234,56 no supermercado com pix",
    "Recebi R$100 de bônus",
    "Gastei 80 reais em cinema no dinheiro",
    "Comprei um carro por R$ 45.000,00",
    "Vendi minha bicicleta por R$ 700,00",
    "Paguei 200 reais no restaurante com pix",
]

for msg in testes:
    try:
        registro = parse_message_ai(msg)
        print(f"{msg} =>\n{registro}\n")
    except Exception as e:
        print(f"{msg} => Erro: {e}")


# Rodar o comando abaixo para executar o teste:
# python -m tests.teste_parser