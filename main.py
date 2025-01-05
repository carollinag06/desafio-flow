from typing import ClassVar
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime, timezone
from typing import Optional, List
from contextlib import asynccontextmanager
from pydantic import BaseModel

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

# Gerenciador de ciclo de vida (lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # Criação das tabelas
    yield  # Ciclo de vida do aplicativo
    SQLModel.metadata.drop_all(engine)  # Exclusão das tabelas quando o app parar

# Inicialização do app com o ciclo de vida
app = FastAPI(lifespan=lifespan)

# Definição do modelo de Tarefa
class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    estado: str = "pendente"
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data_atualizacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    from_attributes: ClassVar[bool] = True  # Adicionando ClassVar

# Definição do modelo para atualização de Tarefa
class TarefaAtualizacao(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    estado: Optional[str]

# Função para fornecer a sessão do banco de dados
def get_session():
    with Session(engine) as session:
        yield session

# Rota para criar uma nova tarefa
@app.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa, session: Session = Depends(get_session)):
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

# Rota para listar todas as tarefas
@app.get("/tarefas/", response_model=List[Tarefa])
def listar_tarefas(session: Session = Depends(get_session)):
    return session.exec(select(Tarefa)).all()

# Rota para obter uma tarefa específica
@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def obter_tarefa(tarefa_id: int, session: Session = Depends(get_session)):
    tarefa = session.get(Tarefa, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# Rota para atualizar uma tarefa existente
@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, tarefa_atualizada: TarefaAtualizacao, session: Session = Depends(get_session)):
    tarefa = session.get(Tarefa, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    for campo, valor in tarefa_atualizada.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)
    tarefa.data_atualizacao = datetime.now(timezone.utc)
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

# Rota para deletar uma tarefa
@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int, session: Session = Depends(get_session)):
    tarefa = session.get(Tarefa, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    session.delete(tarefa)
    session.commit()
