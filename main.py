from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import jwt
from pydantic import BaseModel

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

# Inicializa a aplicação FastAPI
app = FastAPI()

# Variáveis de autenticação
SECRET_KEY = "seu-segredo-aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define o esquema de autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função para gerar o token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta  # Define o tempo de expiração para UTC
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Modelo de Tarefa no banco de dados
class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # O ID é autoincrementado
    titulo: str
    descricao: str
    estado: str = "pendente"
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data_atualizacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Modelo para atualização de dados da tarefa
class TarefaAtualizacao(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    estado: Optional[str]

# Modelo de usuário para autenticação
class User(BaseModel):
    username: str
    password: str

# Rota para login e autenticação com JWT
@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "user" or form_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o token de acesso
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Função para criar uma sessão no banco de dados
def get_session():
    with Session(engine) as session:
        yield session

# Rota para criar uma nova tarefa
@app.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa, session: Session = Depends(get_session)):
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)  # Garante que o ID é atribuído à tarefa
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
    tarefa.data_atualizacao = datetime.now(timezone.utc)  # Atualiza a data de atualização para UTC
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
