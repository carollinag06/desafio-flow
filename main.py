from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Literal
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à minha API de tarefas!"}

# Armazenamento em memória
tarefas = []  # Lista que armazena as tarefas
contador_id = 1  # ID único para cada tarefa

# Modelo Base
class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    estado: Literal["pendente", "em andamento", "concluída"]  # Restrição de valores

# Modelo de Resposta
class TarefaCriada(TarefaBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = ConfigDict(from_attributes=True)

# Modelo de Atualização
class TarefaAtualizacao(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    estado: Optional[Literal["pendente", "em andamento", "concluída"]] = None

# Endpoints
#Criar tarefa(POST)
@app.post("/tarefas/", response_model=TarefaCriada)
def criar_tarefa(tarefa: TarefaBase):
    global contador_id
    nova_tarefa = {
        "id": contador_id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "estado": tarefa.estado,
        "data_criacao": datetime.now(),
        "data_atualizacao": datetime.now(),
    }
    tarefas.append(nova_tarefa)
    contador_id += 1
    return nova_tarefa

# Listar Tarefas (GET)
@app.get("/tarefas/", response_model=List[TarefaCriada])
def listar_tarefas():
    return tarefas

# Visualizar Tarefa Específica (GET)
@app.get("/tarefas/{tarefa_id}", response_model=TarefaCriada)
def obter_tarefa(tarefa_id: int):
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# Atualizar Tarefa (PUT)
@app.put("/tarefas/{tarefa_id}", response_model=TarefaCriada)
def atualizar_tarefa(tarefa_id: int, atualizacao: TarefaAtualizacao):
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    if atualizacao.titulo is not None:
        tarefa["titulo"] = atualizacao.titulo
    if atualizacao.descricao is not None:
        tarefa["descricao"] = atualizacao.descricao
    if atualizacao.estado is not None:
        tarefa["estado"] = atualizacao.estado

    tarefa["data_atualizacao"] = datetime.now()
    return tarefa

# Deletar Tarefa (DELETE)
@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int):
    global tarefas
    tarefa_existente = any(t["id"] == tarefa_id for t in tarefas)
    if not tarefa_existente:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefas = [t for t in tarefas if t["id"] != tarefa_id]
    return {"mensagem": "Tarefa deletada com sucesso"}
