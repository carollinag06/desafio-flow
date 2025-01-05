import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel, select, delete
from main import app, Tarefa, engine

client = TestClient(app)

# Configurando o banco de dados para testes
@pytest.fixture(name="session")
def session_fixture():
    test_engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(test_engine)  # Criação das tabelas
    with Session(test_engine) as session:
        yield session

    # Limpeza do banco após cada teste
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(autouse=True)
def limpar_dados(session):
    session.exec(delete(Tarefa))
    session.commit()

def test_login():
    response = client.post("/login", data={"username": "user", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_criar_tarefa():
    # Gerar token
    login_response = client.post("/login", data={"username": "user", "password": "password"})
    token = login_response.json()["access_token"]

    response = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa 1", "descricao": "Descrição da tarefa"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data  # Verifique se o campo "id" está presente
    assert data["titulo"] == "Tarefa 1"
    assert data["descricao"] == "Descrição da tarefa"
    assert data["estado"] == "pendente"

def test_listar_tarefas(session):
    # Criar tarefas manualmente para o teste
    tarefa1 = Tarefa(titulo="Tarefa 1", descricao="Descrição 1")
    tarefa2 = Tarefa(titulo="Tarefa 2", descricao="Descrição 2")
    session.add_all([tarefa1, tarefa2])
    session.commit()

    response = client.get("/tarefas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["titulo"] == "Tarefa 1"
    assert data[1]["titulo"] == "Tarefa 2"

def test_atualizar_tarefa():
    # Criar uma tarefa para atualizar
    response = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa Antiga", "descricao": "Descrição antiga"}
    )
    tarefa_id = response.json()["id"]  # Garantido que o ID esteja presente

    # Gerar token
    login_response = client.post("/login", data={"username": "user", "password": "password"})
    token = login_response.json()["access_token"]

    response = client.put(
        f"/tarefas/{tarefa_id}",
        json={"titulo": "Tarefa Atualizada", "descricao": "Descrição atualizada", "estado": "em andamento"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Tarefa Atualizada"
    assert data["descricao"] == "Descrição atualizada"
    assert data["estado"] == "em andamento"

def test_deletar_tarefa():
    # Criar uma tarefa para deletar
    response = client.post(
        "/tarefas/",
        json={"titulo": "Tarefa para deletar", "descricao": "Descrição da tarefa"}
    )
    tarefa_id = response.json()["id"]  # Garantido que o ID esteja presente

    # Gerar token
    login_response = client.post("/login", data={"username": "user", "password": "password"})
    token = login_response.json()["access_token"]

    response = client.delete(
        f"/tarefas/{tarefa_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # Verificar se a tarefa foi realmente excluída
    response = client.get(f"/tarefas/{tarefa_id}")
    assert response.status_code == 404
