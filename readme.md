# **API de Gerenciamento de Tarefas (To-Do List) com FastAPI**

**Este projeto é uma API RESTful para gerenciamento de tarefas (To-Do List) desenvolvida utilizando o framework FastAPI. A aplicação suporta as operações CRUD (Criar, Ler, Atualizar e Excluir tarefas) e utiliza JWT (JSON Web Token) para autenticação e segurança.**

## **Funcionalidades**

- **Criar novas tarefas.**
- **Listar todas as tarefas.**
- **Visualizar detalhes de uma tarefa específica.**
- **Atualizar uma tarefa existente.**
- **Excluir tarefas.**
- **Autenticação segura com JWT.**

## **Tecnologias Utilizadas**

- **FastAPI**: Framework moderno para APIs web.
- **Uvicorn**: Servidor ASGI para executar a aplicação.
- **SQLModel**: ORM para interação com o banco de dados SQLite.
- **Pydantic**: Para validação e manipulação de dados.
- **JWT (JSON Web Token)**: Para autenticação.
- **Pytest**: Framework para testes automatizados.
- **SQLite**: Banco de dados relacional embutido.

## **Requisitos**

- **Python 3.8+**
- **pip** (gerenciador de pacotes do Python)

## **Instalação**

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/desafio-flow.git
   cd desafio-flow
   ```

2. **Configure o ambiente virtual (opcional, mas recomendado):**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/MacOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

   **A aplicação estará disponível em** [http://127.0.0.1:8000](http://127.0.0.1:8000).

## **Endpoints Principais**

- **POST /login**: Gera um token JWT ao autenticar o usuário.
- **POST /tasks/**: Cria uma nova tarefa.
- **GET /tasks/**: Lista todas as tarefas do usuário autenticado.
- **GET /tasks/{task_id}**: Retorna os detalhes de uma tarefa específica.
- **PUT /tasks/{task_id}**: Atualiza uma tarefa existente.
- **DELETE /tasks/{task_id}**: Exclui uma tarefa.

## **Documentação da API**

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## **Estrutura do Projeto**

```plaintext
├── .idea/              # Diretório de configuração de projeto do IDE (possivelmente PyCharm).
├── __pycache__/        # Diretório de cache gerado pelo Python (arquivos compilados).
├── app/
│   ├── main.py         # **Arquivo principal da aplicação**
│   ├── auth.py         # **Gerenciamento de autenticação com JWT**
│   ├── models.py       # **Modelos de dados e esquemas**               # Diretório principal contendo o código-fonte da aplicação.
├── venv/               # Ambiente virtual Python com bibliotecas instaladas.
├── .gitattributes      # Configuração para controle de versões (Git).
├── LICENSE             # Arquivo de licença do projeto.
├── readme.md           # Documentação do projeto, atualizada recentemente.
├── requirements.txt    # Dependências necessárias para rodar o projeto.
├── tarefas.db          # Banco de dados SQLite utilizado pela aplicação.
├── test.db             # Banco de dados de teste para desenvolvimento.
├── test_main.py        # Arquivo contendo testes automatizados.

```

## **Testes**

**Para rodar os testes:**

```bash
pytest
```

## **Licença**

**Este projeto está licenciado sob a MIT License.**

