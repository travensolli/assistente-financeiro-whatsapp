# Assistente Financeiro no WhatsApp

Este projeto é um assistente financeiro que utiliza o WhatsApp como interface de comunicação. Ele permite registrar transações financeiras, como gastos e receitas, e armazena essas informações em uma planilha do Google Sheets.

## Funcionalidades
- Receber mensagens via WhatsApp utilizando a API Twilio.
- Processar mensagens para identificar tipo, descrição, valor e método de pagamento.
- Registrar transações financeiras em uma planilha do Google Sheets.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados e configurados:

1. **Python 3.10 ou superior**
2. **Conta no Twilio** com um número de WhatsApp configurado.
3. **Google Sheets API** habilitada e um arquivo `credentials.json` para autenticação.
4. **Ngrok** para expor o servidor local para a internet durante os testes.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/assistente-financeiro-whatsapp.git
   cd assistente-financeiro-whatsapp
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```env
   TWILIO_ACCOUNT_SID=seu_account_sid_aqui
   TWILIO_AUTH_TOKEN=seu_auth_token_aqui
   TWILIO_WHATSAPP_NUMBER=seu_numero_whatsapp_aqui
   GOOGLE_CREDS_JSON=conteúdo do arquivo credentials.json caso quero realizar deploy
   ```

5. Adicione o arquivo `credentials.json` na raiz do projeto para autenticação com a Google Sheets API.

## Execução

1. Inicie o servidor FastAPI:
   ```bash
   uvicorn src.bot:app --reload --port 8000
   ```

2. Inicie o Ngrok para expor o servidor local:
   ```bash
   ngrok http 8000
   ```

3. Configure o webhook no Twilio:
   - Acesse o painel do Twilio.
   - Configure o URL do webhook para o endpoint gerado pelo Ngrok, adicionando `/webhook` ao final. Exemplo:
     ```
     https://<seu-subdominio-ngrok>.ngrok.io/webhook
     ```

4. Envie mensagens para o número do WhatsApp configurado no Twilio e veja o assistente financeiro em ação.

## Testes

1. Para rodar os testes, execute:
   ```bash
   python -m unittest discover tests
   ```

2. Certifique-se de que os testes estão passando para validar o funcionamento do projeto.

## Estrutura do Projeto

```
assistente-financeiro-whatsapp/
├── credentials.json          # Credenciais para a Google Sheets API
├── README.md                 # Documentação do projeto
├── requirements.txt          # Dependências do projeto
├── src/                      # Código-fonte principal
│   ├── bot.py                # Servidor FastAPI
│   ├── config.py             # Configurações do projeto
│   ├── models.py             # Modelos de dados
│   ├── parser.py             # Processamento de mensagens
│   ├── sheets.py             # Integração com Google Sheets
├── tests/                    # Testes do projeto
│   ├── teste_parser.py       # Testes para o parser
│   ├── teste_sheets.py       # Testes para integração com Google Sheets
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.