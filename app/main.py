from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
from uuid import uuid4  # Importação para gerar IDs únicos para as tarefas

# Inicialização da aplicação FastAPI
app = FastAPI()

# Simulação de um banco de dados na memória
tasks_db = []

# Classe base para representar os dados de uma tarefa
class TaskBase(BaseModel):
    titulo: str  # Título da tarefa (obrigatório)
    descricao: Optional[str] = None  # Descrição da tarefa (opcional)
    estado: str  # Estado da tarefa (obrigatório: pendente, em andamento ou concluída)

# Classe para criação de uma nova tarefa
class TaskCreate(TaskBase):
    pass

# Classe para representar a resposta de uma tarefa, incluindo campos adicionais
class TaskResponse(TaskBase):
    id: str  # ID único da tarefa
    data_criacao: datetime  # Data de criação da tarefa
    data_atualizacao: Optional[datetime] = None  # Data da última atualização da tarefa (opcional)

# Endpoint para criar uma nova tarefa
@app.post("/tasks/", response_model=TaskResponse, summary="Criar tarefas")
def create_task(task: TaskCreate):
    """
    Cria uma nova tarefa com os dados fornecidos.
    Gera automaticamente um ID único e registra a data de criação.
    """
    new_task = {
        "id": str(uuid4()),  # Geração de ID único
        "titulo": task.titulo,
        "descricao": task.descricao,
        "estado": task.estado,
        "data_criacao": datetime.now(timezone.utc),  # Data atual com fuso horário UTC
        "data_atualizacao": None,  # Inicialmente sem data de atualização
    }
    tasks_db.append(new_task)  # Adiciona a nova tarefa ao banco de dados
    return new_task

# Endpoint para listar todas as tarefas
@app.get("/tasks/", response_model=List[TaskResponse], summary="Listar todas as tarefas")
def list_tasks():
    """
    Retorna a lista de todas as tarefas armazenadas no banco de dados.
    """
    return tasks_db

# Endpoint para visualizar os detalhes de uma tarefa específica
@app.get("/tasks/{task_id}", response_model=TaskResponse, summary="Visualizar uma tarefa específica")
def get_task(task_id: str):
    """
    Busca uma tarefa específica pelo ID.
    Retorna erro 404 caso a tarefa não seja encontrada.
    """
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task

# Endpoint para atualizar uma tarefa existente
@app.put("/tasks/{task_id}", response_model=TaskResponse, summary="Atualizar uma tarefa existente")
def update_task(task_id: str, updated_task: TaskCreate):
    """
    Atualiza os dados de uma tarefa existente com base no ID fornecido.
    Atualiza também a data de modificação da tarefa.
    """
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task.update(updated_task.model_dump())  # Atualiza os dados da tarefa
    task["data_atualizacao"] = datetime.now(timezone.utc)  # Define a data de atualização
    return task

# Endpoint para deletar uma tarefa existente
@app.delete("/tasks/{task_id}", summary="Deletar uma tarefa")
def delete_task(task_id: str):
    """
    Remove uma tarefa do banco de dados com base no ID fornecido.
    """
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]  # Remove a tarefa pelo ID
    return {"message": "Tarefa deletada com sucesso!"}
