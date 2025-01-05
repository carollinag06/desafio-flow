Olá esse projeto é de uma api de gerenciamento de tarefa

1. Inicie o servidor FastAPI:

   ```bash
   uvicorn main:app --reload
   ```

2. Acesse a documentação interativa da API:

   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

3. A API estará rodando localmente em: [http://127.0.0.1:8000](http://127.0.0.1:8000).

## **Testes**

1. Instale o Pytest:

   ```bash
   pip install pytest
   ```

2. Execute os testes:

   ```bash
   pytest
   ```

## **Estrutura do Projeto**

```
<RAIZ_DO_PROJETO>/
├── main.py          # Código principal da aplicação
├── requirements.txt # Dependências do projeto
├── README.md        # Instruções do projeto
└── tests/           # Diretório contendo testes (opcional)
```

## **Dependências**

- **FastAPI**: Framework para criação de APIs.
- **Uvicorn**: Servidor ASGI para rodar o FastAPI.

## **Contribuição**

Sinta-se à vontade para contribuir com melhorias. Faça um fork do projeto, crie uma branch, implemente suas alterações e envie um Pull Request!

## **Licença**

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.