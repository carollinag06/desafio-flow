from fastapi.testclient import TestClient
from app.main import app
# Cria um cliente de teste para a aplicação
client = TestClient(app)

# Teste de criação de tarefas
def test_create_task():
    """
    Testa a criação de uma nova tarefa.
    """
    response = client.post("/tasks/", json={"titulo": "Teste", "descricao": "Descrição", "estado": "pendente"})
    assert response.status_code == 200
    assert response.json()["titulo"] == "Teste"

# Teste de listagem de tarefas
def test_list_tasks():
    """
    Testa a listagem de todas as tarefas.
    """
    response = client.get("/tasks/")
    assert response.status_code == 200

# Teste de visualização de uma tarefa específica
def test_get_task():
    """
    Testa a recuperação de uma tarefa pelo ID.
    """
    response = client.post("/tasks/", json={"titulo": "Teste", "descricao": "Descrição", "estado": "pendente"})
    task_id = response.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Teste"

# Teste de atualização de tarefas
def test_update_task():
    """
    Testa a atualização de uma tarefa existente.
    """
    response = client.post("/tasks/", json={"titulo": "Teste", "descricao": "Descrição", "estado": "pendente"})
    task_id = response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"titulo": "Atualizado", "descricao": "Nova descrição", "estado": "concluída"})
    assert response.status_code == 200
    assert response.json()["titulo"] == "Atualizado"

# Teste de exclusão de tarefas
def test_delete_task():
    """
    Testa a exclusão de uma tarefa pelo ID.
    """
    response = client.post("/tasks/", json={"titulo": "Teste", "descricao": "Descrição", "estado": "pendente"})
    task_id = response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Tarefa deletada com sucesso!"}
