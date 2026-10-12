# 🎢 Sistema de Reservas de Parque Temático

Projeto desenvolvido para a disciplina de **Algoritmos e Estruturas de Dados**, com foco na aplicação de **Programação Orientada a Objetos** e **estruturas de dados implementadas pelo próprio grupo**.

O sistema tem como objetivo simular o gerenciamento de um parque temático, permitindo trabalhar com **atrações, visitantes, reservas e filas virtuais**, incluindo regras de prioridade para visitantes com passes especiais.

## 📌 Sobre o projeto

A aplicação será desenvolvida em **Python** e contará com uma **interface gráfica utilizando CustomTkinter**.

Entre as principais funcionalidades previstas estão:

* gerenciamento de atrações;
* cadastro e gerenciamento de visitantes;
* criação e gerenciamento de reservas;
* filas virtuais para as atrações;
* tratamento de prioridades nas filas;
* consulta da posição dos visitantes;
* painel de controle para administração do parque;
* portal para interação dos visitantes;
* apresentação de métricas do funcionamento do sistema.

## 🧩 Estruturas de Dados

Um dos principais objetivos do projeto é aplicar, na prática, os conteúdos estudados na disciplina.

As estruturas de dados utilizadas na parte principal do sistema serão **implementadas pelo próprio grupo**, com destaque para:

* listas encadeadas;
* filas;
* outras estruturas auxiliares que sejam necessárias ao funcionamento do sistema.

A implementação deverá respeitar as regras da atividade, evitando utilizar diretamente estruturas prontas da linguagem para substituir as estruturas que precisam ser desenvolvidas pelo grupo.

## 🏗️ Organização do projeto

O projeto está organizado para separar as principais responsabilidades da aplicação:

src/
├── gui/          # Interface gráfica (telas)
├── models/       # Classes e entidades do sistema
├── services/     # Regras e operações do sistema
├── structures/   # Estruturas de dados implementadas pelo grupo
├── database/     # Persistência em SQLite
└── main.py       # Ponto de entrada da aplicação

tests/            # Testes manuais + seeds de dados
data/             # Banco de dados SQLite (não versionado)
docs/             # Documentação

## 🚀 Como rodar o projeto

### Requisitos

* Python 3.12 ou superior
* Linux, macOS ou Windows (testado em Linux Mint XFCE)
* Não é necessária nenhuma instalação externa de banco de dados — o projeto usa **SQLite**, que já vem embutido no Python.

### 1. Clonar o repositório

git clone https://github.com/luhanfelipe/theme-park-reservation-system.git
cd theme-park-reservation-system

### 2. Criar e ativar o ambiente virtual

python3 -m venv .venv
source .venv/bin/activate

**No Windows, a ativação é:**

.venv\Scripts\activate

### 3. Instalar as dependências

pip install -r requirements.txt

### 4. Rodar a aplicação

python -m src.main

Uma janela de login deve abrir. Use as credenciais fornecidas na disciplina ou as definidas em src/gui/tela_login.py.


## 🌱 Popular o banco com dados reais
O sistema começa com o banco vazio. Para carregar os dados de demonstração do Thorpe Park (parque temático real no Reino Unido), rode os dois seeds:

### Popular as atrações

python -m tests.seed_thorpe_park

Isso insere 8 atrações reais do parque (SAW – The Ride, The Walking Dead: The Ride, Hyperia, Stealth, entre outras).

### Popular os visitantes

python -m tests.seed_visitantes
Isso insere 20 visitantes fictícios (10 brasileiros e 10 gringos), com passes variados (VIP, Anual e Normal) e idades entre 8 e 55 anos.

### Observações
- Os dois seeds são idempotentes: podem ser rodados várias vezes sem duplicar registros.
- O banco fica em data/parque.db e não é versionado (está no .gitignore).
- Para resetar o banco: rm data/parque.db. Na próxima execução do sistema, ele é recriado automaticamente.

## 🛠️ Tecnologias

* **Python 3.12**
* **CustomTkinter** (interface gráfica)
* **SQLite** (persistência local, embutido no Python)
* **Git e GitHub**

## 🚧 Status

**Em desenvolvimento ativo.**

Já implementado:

* Modelos de visitante e atração;
* Lista encadeada e fila de prioridade (implementadas pelo grupo);
* Serviço central (`ParqueService`) com regras de negócio;
* Interface gráfica com telas de login, dashboard, cadastro de visitante, cadastro de atração e fila virtual;
* Persistência em SQLite (dados sobrevivem ao fechar e reabrir o sistema);
* Testes manuais das estruturas e do serviço.

Próximas etapas previstas: histórico de visitas, painel de controle com métricas e portal do visitante.

## 👥 Desenvolvimento

Projeto desenvolvido em grupo para a disciplina de **Algoritmos e Estruturas de Dados**.

> Este README é provisório e será atualizado conforme novas funcionalidades, estruturas e decisões de projeto forem implementadas.
