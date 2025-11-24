# 🌱 AgroConecta  
Sistema web para gestão de sementes, armazéns, cooperativas, lotes, solicitações e usuários.  
Desenvolvido como parte do **Projeto Integrador — SENAC**.

---

## 📌 Visão Geral

O **AgroConecta** centraliza e facilita o gerenciamento de todo o processo de distribuição de sementes entre gestores, cooperativas, produtores e armazéns.

### O sistema permite:
- Cadastro de cooperativas  
- Armazéns + operadores  
- Tipos de sementes  
- Lotes com QR Code  
- Solicitações de distribuição  
- Dashboard analítico  
- Login e controle de usuários  
- Exclusões com verificação de dependências  

---

# 🚀 Funcionalidades Principais

### 👤 Gestão de Usuários
- Login de Gestor e Operador  
- Edição de perfil  
- Controle de acesso  

### 🏬 Gestão de Armazéns
- Cadastro completo  
- Edição sem duplicar endereços  
- Operador vinculado  
- Exclusão com bloqueio se houver lotes vinculados  

### 🌾 Gestão de Sementes
- Cadastro dos tipos de sementes  

### 📦 Gestão de Lotes
- Entrada de lote  
- QR Code  
- Edição  
- Exclusão  
- Detalhamento  

### 📝 Gestão de Solicitações
- Lista de solicitações  
- Alteração de status  
- Visualização de cooperativa, quantidade, safra, etc.  

### 📊 Dashboard Analítico
- Peso total de sementes por armazém  
- Quantidade de solicitações por status  
- Lotes cadastrados nos últimos 6 meses  

---

# 🛠️ Como Rodar Localmente

## 1. Clone o repositório

git clone https://github.com/AndersonBem/AgroConecta.git
cd AgroConecta

## 2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
OU:
source venv/bin/activate  # Linux/Mac

## 3. Instale as dependências
pip install -r requirements.txt

## 4. Configure o MySQL

Crie o banco:

CREATE DATABASE AgroConecta;
USE AgroConecta;

Importe o arquivo SQL:
SOURCE caminho/do/arquivo.sql;

## 5. Configure o Django (settings.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AgroConecta',
        'USER': 'root',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

## 6. Migre o banco
python manage.py migrate

## 7. Rode o servidor
python manage.py runserver

Acesse em:
👉 http://127.0.0.1:8000/


## 📉 Dashboard Analítico

O dashboard usa Chart.js com dados vindos do Django:

🌾 Sementes por armazém

📑 Status das solicitações

📦 Lotes por mês (últimos 6 meses)

Todos os dados são convertidos para JSON seguro no template.

👥 Equipe

Anderson Bem — Back-end e banco

Wendell Barboza — Front-end e design

## 📄 Licença

Projeto acadêmico — Livre para uso educacional.




