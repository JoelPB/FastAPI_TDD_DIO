# FastAPI_TDD_DIO
## Desafio de projeto da DIO [Criando Uma API Com FastAPI Utilizando TDD](https://web.dio.me/lab/tdd-com-python/learning/74532065-425a-48bb-bf95-9ffa34ad8f43)
[Link para o repositório da DIO](https://github.com/digitalinnovationone/store_api)
---

## Instalando o Invoke Para automação de tarefas
Para usar o invoke, você precisa instalá-lo no ambiente do seu projeto Python. Você pode fazer isso usando o pip, o gerenciador de pacotes Python.

Abra o terminal do PyCharm e execute o seguinte comando:

```
pip install invoke
```
## Usando o Invoke
Após a instalação do invoke, você pode criar um arquivo tasks.py no diretório raiz do seu projeto para definir suas tarefas. Para configurar o invoke para um projeto FastAPI com Uvicorn, você pode criar tarefas no arquivo tasks.py para iniciar o servidor Uvicorn e realizar outras tarefas relacionadas ao desenvolvimento do seu projeto.

Linhas de comando utilizadas:

Rodando o projeto
````commandline
invoke start
````
Instalando o pre-commit
````commandline
invoke precommit-install
````
