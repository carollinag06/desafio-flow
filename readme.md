API de Gerenciamento de Tarefas (To-Do List) com FastAPI

Este projeto é uma API RESTful para gerenciamento de tarefas (To-Do List) desenvolvida utilizando o framework FastAPI. A aplicação suporta as operações CRUD (Criar, Ler, Atualizar e Excluir tarefas) e utiliza JWT (JSON Web Token) para autenticação e segurança.

Funcionalidades

Criar novas tarefas.

Listar todas as tarefas.

Visualizar detalhes de uma tarefa específica.

Atualizar uma tarefa existente.

Excluir tarefas.

Autenticação segura com JWT.

Tecnologias Utilizadas

FastAPI: Framework moderno para APIs web.

Uvicorn: Servidor ASGI para executar a aplicação.

SQLModel: ORM para interação com o banco de dados SQLite.

Pydantic: Para validação e manipulação de dados.

JWT (JSON Web Token): Para autenticação.

Pytest: Framework para testes automatizados.

SQLite: Banco de dados relacional embutido.

Requisitos

Python 3.8+

pip (gerenciador de pacotes do Python)

Instalação

Clone o repositório:

git clone https://github.com/seu-usuario/desafio-flow.git
cd desafio-flow

Configure o ambiente virtual (opcional, mas recomendado):

Windows:

python -m venv venv
venv\Scripts\activate

Linux/MacOS:

python3 -m venv venv
source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

Inicie o servidor:

uvicorn app.main:app --reload

A aplicação estará disponível em http://127.0.0.1:8000.

Endpoints Principais

POST /login: Gera um token JWT ao autenticar o usuário.

POST /tasks/: Cria uma nova tarefa.

GET /tasks/: Lista todas as tarefas do usuário autenticado.

GET /tasks/{task_id}: Retorna os detalhes de uma tarefa específica.

PUT /tasks/{task_id}: Atualiza uma tarefa existente.

DELETE /tasks/{task_id}: Exclui uma tarefa.

Documentação da API

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

Estrutura do Projeto

├── app/
│   ├── main.py        # Arquivo principal da aplicação
│   ├── auth.py        # Gerenciamento de autenticação com JWT
│   ├── models.py      # Modelos de dados e esquemas
│   ├── crud.py        # Operações no banco de dados
│   ├── database.py    # Configuração do banco de dados
├── test_main.py       # Testes automatizados com Pytest
├── requirements.txt   # Dependências do projeto
├── .env               # Configurações de ambiente
├── README.md          # Documentação do projeto

Testes

Para rodar os testes:

pytest

Licença

Este projeto está licenciado sob a MIT License.
