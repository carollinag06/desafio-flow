from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, List, Literal
from datetime import datetime

# Configuração do banco SQLite
DATABASE_URL = "sqlite:///tarefas.db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para exibir os logs SQL no console

app = FastAPI()


# Modelo representando a tabela no banco de dados
class Tarefa(SQLModel, table=True):  # table=True indica que é uma tabela no banco
    id: Optional[int] = Field(default=None, primary_key=True)  # ID autoincrementado
    titulo: str
    descricao: Optional[str] = None
    estado: Literal["pendente", "em andamento", "concluída"]  # Restrição de valores
    data_criacao: datetime = Field(default_factory=datetime.utcnow)  # Padrão: agora
    data_atualizacao: datetime = Field(default_factory=datetime.utcnow)


# Função para criar as tabelas no banco
def criar_tabelas():
    SQLModel.metadata.create_all(engine)


# Criar tabelas ao iniciar o aplicativo
@app.on_event("startup")
def ao_iniciar():
    criar_tabelas()


# Rota principal
@app.get("/")
def home():
    return {"mensagem": "Beem-vindo à minha API de tarefas!"}


# Endpoints

# Criar uma nova tarefa
@app.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa):
    with Session(engine) as session:
        # Adiciona a nova tarefa
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)  # Atualiza a tarefa com o ID gerado
        return tarefa


# Listar todas as tarefas
@app.get("/tarefas/", response_model=List[Tarefa])
def listar_tarefas():
    with Session(engine) as session:
        tarefas = session.query(Tarefa).all()  # Busca todas as tarefas
        return tarefas


# Visualizar uma tarefa específica
@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def obter_tarefa(tarefa_id: int):
    with Session(engine) as session:
        tarefa = session.get(Tarefa, tarefa_id)  # Busca a tarefa pelo ID
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return tarefa


# Atualizar uma tarefa
@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, atualizacao: Tarefa):
    with Session(engine) as session:
        tarefa = session.get(Tarefa, tarefa_id)
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")

        # Atualiza os campos da tarefa
        for key, value in atualizacao.dict(exclude_unset=True).items():
            setattr(tarefa, key, value)

        tarefa.data_atualizacao = datetime.utcnow()  # Atualiza a data
        session.commit()
        session.refresh(tarefa)
        return tarefa


# Deletar uma tarefa
@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int):
    with Session(engine) as session:
        tarefa = session.get(Tarefa, tarefa_id)
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        session.delete(tarefa)
        session.commit()
    return {"mensagem": "Tarefa deletada com sucesso"}
