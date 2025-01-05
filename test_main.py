from fastapi.testclient import TestClient
from main import app  # Importa o FastAPI do seu código principal

client = TestClient(app)  # Instancia o cliente de testes

def test_home():
    response = client.get("/")  # Faz uma requisição GET para o endpoint "/"
    assert response.status_code == 200  # Verifica se o status é 200 (OK)
    assert response.json() == {"mensagem": "Bem-vindo à minha API de tarefas!"}  # Verifica a mensagem retornada


def test_criar_tarefa():
    # Dados para criar uma tarefa
    nova_tarefa = {
        "titulo": "Estudar Python",
        "descricao": "Aprender a usar Pytest",
        "estado": "pendente"
    }

    # Envia uma requisição POST com os dados da tarefa
    response = client.post("/tarefas/", json=nova_tarefa)

    # Verifica se o status de resposta é 200
    assert response.status_code == 200

    # Verifica os dados retornados pela API
    resultado = response.json()
    assert resultado["titulo"] == nova_tarefa["titulo"]
    assert resultado["descricao"] == nova_tarefa["descricao"]
    assert resultado["estado"] == nova_tarefa["estado"]
    assert "id" in resultado  # O ID deve estar presente
    assert "data_criacao" in resultado  # A data de criação deve estar presente


def test_listar_tarefas():
    # Faz uma requisição GET para listar as tarefas
    response = client.get("/tarefas/")

    # Verifica se o status de resposta é 200
    assert response.status_code == 200

    # Verifica se a resposta é uma lista
    tarefas = response.json()
    assert isinstance(tarefas, list)
    assert len(tarefas) > 0  # Verifica se a lista contém pelo menos uma tarefa


def test_obter_tarefa():
    # Faz uma requisição GET para obter a tarefa com ID 1
    response = client.get("/tarefas/1")

    # Verifica se o status de resposta é 200
    assert response.status_code == 200

    # Verifica os dados da tarefa retornada
    tarefa = response.json()
    assert tarefa["id"] == 1
    assert "titulo" in tarefa
    assert "estado" in tarefa


def test_atualizar_tarefa():
    # Dados para atualizar o estado da tarefa
    atualizacao = {"estado": "em andamento"}

    # Faz uma requisição PUT para atualizar a tarefa com ID 1
    response = client.put("/tarefas/1", json=atualizacao)

    # Verifica se o status de resposta é 200
    assert response.status_code == 200

    # Verifica os dados atualizados da tarefa
    tarefa_atualizada = response.json()
    assert tarefa_atualizada["id"] == 1
    assert tarefa_atualizada["estado"] == "em andamento"


def test_deletar_tarefa():
    # Faz uma requisição DELETE para excluir a tarefa com ID 1
    response = client.delete("/tarefas/1")

    # Verifica se o status de resposta é 204 (No Content)
    assert response.status_code == 204

    # Verifica se a tarefa foi realmente excluída
    response = client.get("/tarefas/1")
    assert response.status_code == 404  # A tarefa não deve mais existir






def test_criar_tarefa_estado_invalido():
    # Dados com um estado inválido
    tarefa_invalida = {
        "titulo": "Tarefa inválida",
        "descricao": "Teste com estado inválido",
        "estado": "finalizado"  # Estado inválido
    }

    # Faz uma requisição POST para criar a tarefa
    response = client.post("/tarefas/", json=tarefa_invalida)

    # Verifica se o código de resposta é 422
    assert response.status_code == 422

    # Verifica se a mensagem de erro é clara
    resposta_json = response.json()
    assert resposta_json["detail"][0]["msg"] == "Input should be 'pendente', 'em andamento' or 'concluída'"


def test_atualizar_tarefa_inexistente():
    # Dados para atualizar
    atualizacao = {
        "titulo": "Título Atualizado",
        "descricao": "Descrição Atualizada",
        "estado": "em andamento",
    }

    # ID inexistente
    tarefa_id_inexistente = 999

    # Faz uma requisição PUT para atualizar a tarefa
    response = client.put(f"/tarefas/{tarefa_id_inexistente}", json=atualizacao)

    # Verifica se o código de resposta é 404
    assert response.status_code == 404

    # Verifica se a mensagem de erro indica que a tarefa não foi encontrada
    assert response.json() == {"detail": "Tarefa não encontrada"}
