# 🚀 Assistente Financeiro WhatsApp + Google Sheets

Automatize seu controle financeiro registrando **gastos e ganhos via WhatsApp** que vão direto para o Google Sheets. Basta enviar uma mensagem no WhatsApp e o bot reconhece, interpreta e salva as transações de forma automática!  
Este projeto é robusto, gratuito, personalizável e pronto para ser usado por qualquer dev que queira ter mais controle financeiro sem fricção.

## 🔥 Principais Funcionalidades

- 📲 **Integração WhatsApp (Twilio):** envie mensagens como “Gastei R$ 20 no mercado” e o bot entende, responde e registra.
- 📑 **Armazenamento direto no Google Sheets:** histórico acessível de qualquer lugar.
- 🤖 **NLP & Inteligência:** reconhecimento de diferentes formas de valores, descrições, meios de pagamento, etc.
- 🚀 **Deploy grátis em nuvem (Railway):** sem custos para rodar 24/7.
- 📦 **Pronto para expandir:** comandos de saldo, extrato, múltiplos usuários, etc.

<!--
## ✨ Demonstração

![demonstração do fluxo WhatsApp para Google Sheets](docs/demo.gif)  
*Envie sua mensagem no WhatsApp e pronto: saldo, ganhos e gastos na planilha!*
-->

## 🛠️ Como funciona?

1. Você envia uma mensagem **por WhatsApp**
2. O **Twilio** encaminha para o webhook (FastAPI)
3. O backend processa com **spaCy / price-parser**
4. O gasto/ganho é salvo no **Google Sheets**
5. Você recebe uma confirmação no WhatsApp

## 📋 Pré-requisitos

- Conta no [Twilio](https://www.twilio.com/try-twilio) (usando modo sandbox)
- Conta Google (para Google Sheets)
- Python 3.8+ e pip
- Respeitar boas práticas de uso de credenciais!

## 🚧 Como rodar do zero (passo a passo)

Siga esses passos para configurar e executar essa aplicação no seu computador de forma fácil e rápida.

### 1. Clone o repositório

```bash
git clone https://github.com/travensolli/assistente-financeiro-whatsapp.git
cd assistente-financeiro-whatsapp
```

### 2. Monte o ambiente Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```
### 3. Prepare o Google Sheets

- Crie uma planilha com aba chamada `Registros` com as colunas: Data, Tipo, Descrição, Valor, Pagamento
- No Google Cloud, ative a Google Sheets API
- Gere um arquivo `credentials.json` (conta de serviço) e compartilhe a planilha com o e-mail da conta de serviço
- **COPIE o conteúdo do `credentials.json` em uma variável de ambiente depois!** (não suba o arquivo pro git)

### 4. Configurando variáveis de ambiente (.env)

Crie o arquivo `.env` na raiz do projeto com:

```dotenv
# Twilio
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Google Sheets (contéudo inteiro do arquivo credentials.json)
GOOGLE_CREDS_JSON={"type": "service_account", "...": "..."}
   ```
Importante: Nunca suba esse arquivo ao seu git.

### 5. Execute o backend localmente

Rode o projeto com o comando:

```bash
uvicorn src.bot:app --reload --port 8000
```
### 6. Utilizando ngrok para webhook local

Para testes locais, use o ngrok para receber requisições externas:

```bash
ngrok http 8000
   ```
Copie a URL gerada pelo ngrok e configure como webhook (com /webhook) no painel Twilio.

### 7. Teste enviando suas mensagens pelo WhatsApp

Envie mensagens para o número WhatsApp configurado no Twilio e veja os dados sendo registrados automaticamente na sua planilha Google Sheets.

## 🧪 Testes

1. Para executar os testes unitários, rode o comando:

```bash
python -m unittest discover tests
```

#### Certifique-se que todos os testes estão passando antes de seguir para deploy ou modificar funcionalidades.

## 📁 Estrutura do Projeto

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
## 🚀 Deploy gratuito em Produção (Railway)

1. Suba suas modificações para o GitHub.
2. No [Railway](https://railway.app/), conecte seu repositório GitHub num novo projeto.
3. Configure no Railway o comando de start como:

```bash
uvicorn src.bot:app --host 0.0.0.0 --port $PORT
```

4. Configure as variáveis de ambiente (GOOGLE_CREDS_JSON, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, etc.) no painel do Railway.

5. Após deploy concluído, pegue a sua URL pública fornecida pelo Railway e ajuste seu webhook no Twilio para esta URL pública + /webhook.

## 🔐 Dicas de Segurança

- Jamais envie arquivos sensíveis (`credentials.json`, `.env`) para seu GitHub. Use variáveis de ambiente.
- Revise periodicamente permissões e logs do Railway e Twilio para garantir segurança das integrações.

## 🧩 Próximos passos e melhorias futuras

- Comandos adicionais no WhatsApp (ex.: "saldo", "extrato mensal").
- Suporte a múltiplos usuários/plataformas.
- Inserção de gráficos e análises automáticas na planilha.

## 🤝 Contribuindo com o projeto

Sugestões de melhorias, bugs encontrados, novos recursos ou qualquer questionamento são muito bem-vindos!  
Sinta-se livre para criar Issues e Pull Requests ou me chamar para discutir qualquer ideia relacionada ao projeto.


## 📫 Contato

Criado por: [Gabriel Travensolli](https://www.linkedin.com/in/gabrieltravensolli/)  
Email: g.travensolli@gmail.com  
GitHub: [travensolli](https://github.com/travensolli)