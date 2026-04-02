# 🧠 Nucleus - Resumidor de Documentos com IA

Aplicação web Flask que permite fazer upload de documentos (PDF ou TXT) e gerar resumos usando IA (Groq/Llama ou Google Gemini).

## 📋 Funcionalidades

- ✅ Upload de documentos PDF e TXT
- ✅ Três tipos de resumo: Curto, Detalhado e Bullet Points
- ✅ Três opções de IA: Groq (Llama 3.3), Google Gemini e OpenAI (ChatGPT)
- ✅ Interface limpa e responsiva
- ✅ Processamento em tempo real
- ✅ Suporte a formatação Markdown nos resumos

## 🚀 Instalação

### 1. Clone o repositório ou navegue até a pasta do projeto

```bash
cd /home/linc/nucleus
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/Mac
# ou
venv\Scripts\activate  # No Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as chaves de API

Edite o arquivo `.env` e adicione suas chaves de API:

```env
GROQ_API_KEY=sua_chave_groq_aqui
GEMINI_API_KEY=sua_chave_gemini_aqui
```

**Onde obter as chaves:**
- Groq: https://console.groq.com/keys
- Gemini: https://makersuite.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

### 5. Execute a aplicação

**Opção 1: Usando o script run.sh**
```bash
./run.sh
```

**Opção 2: Manualmente**
```bash
source venv/bin/activate  # Ative o ambiente virtual primeiro
python app.py
```

A aplicação estará disponível em: http://localhost:5000

## 📖 Como Usar

1. Acesse http://localhost:5000 no navegador
2. Selecione um arquivo PDF ou TXT
3. Escolha o tipo de resumo desejado
4. Selecione a IA (Groq ou Gemini)
5. Clique em "Gerar Resumo"
6. Aguarde o processamento e veja o resultado

## 📁 Estrutura do Projeto

```
nucleus/
├── app.py                 # Lógica principal Flask
├── templates/
│   └── index.html        # Interface do usuário
├── static/               # Arquivos estáticos (criado automaticamente)
├── uploads/              # Pasta temporária para uploads (criada automaticamente)
├── .env                  # Chaves de API (não commitar!)
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Flask** - Framework web Python
- **PyPDF2** - Extração de texto de PDFs
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **requests** - Chamadas HTTP para APIs
- **google-generativeai** - SDK do Google Gemini

## 🔒 Segurança

- Nunca commite o arquivo `.env` com suas chaves de API
- Limite de tamanho de arquivo: 16MB
- Arquivos temporários são deletados após processamento
- Texto limitado a 15.000 caracteres para evitar limites de API

## 📝 Notas

- Certifique-se de ter pelo menos uma chave de API configurada
- PDFs com imagens podem não ter todo o texto extraído
- O tempo de processamento varia conforme o tamanho do documento

## 🐛 Troubleshooting

**Erro: "GROQ_API_KEY not configured"**
- Verifique se adicionou a chave no arquivo `.env`

**Erro ao extrair texto do PDF**
- Verifique se o PDF não está protegido ou corrompido

**Erro de conexão com API**
- Verifique sua conexão com a internet
- Confirme se as chaves de API estão válidas