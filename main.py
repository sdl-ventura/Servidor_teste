from fastapi import FastAPI #importa FastAPI pra criar a API 
from fastapi.responses import HTMLResponse 
import psycopg2 # conexão com o banco de dados online
import csv #biblioteca para ler a planilha de arquivos
import os
from dotenv import load_dotenv


load_dotenv() #carrega meu acesso ao neon/fastApi

app = FastAPI() #cria a API

DATABASE_URL = os.getenv("DATABASE_URL")

conexao = psycopg2.connect(DATABASE_URL)
# cria a conexão com o meu projeto do Neon (conexao com SQL, https, etc etc etc)

cursor = conexao.cursor() #envia comandos SQL (linguagem do banco de dados)




cursor.execute("""
CREATE TABLE IF NOT EXISTS dados(
            id SERIAL PRIMARY KEY,
            tema TEXT,
            pergunta TEXT,
            resposta TEXT
            )
""") #cria uma tabela de usuários com SQL 


with open("dados.csv", newline="", encoding="utf-8") as arquivo:

    leitor = csv.reader(arquivo)

    next(leitor)

    for linha in leitor:

        pergunta = linha[0]
        resposta = linha[1]

        cursor.execute(
            """
            INSERT INTO dados (pergunta, resposta)
            VALUES (%s, %s)
            """,
            (pergunta, resposta)
        )

conexao.commit()




# página inicial, me leva à função inicio

@app.get("/", response_class=HTMLResponse)

#retorna a letra de Holligan na página inicial
def inicio():

    return """
    <html>
        <head>
            <title>Meu Servidor</title>
        </head>

        <body style="
            background-color: violet;
            color: white;
            font-family: Arial;
            text-align: center;
            padding-top: 100px;
        ">

            <h1>🌌 SdL </h1>
            <img
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXlKjV9LJbM2rKMZJ7hXSmgsQstVCOZilswP0fz_pozi-2J1A7v_Li7-pkc6TDfspJ9rtlF3wvuzqo0FPawekAgTem_G36_HKOAijt8A&s=10"
                width="800"

            </p>

            </p>

            <a href="/Banco_de_dados_SdL_AI">
                Ver Banco de Dados
            </a>

        </body>
    </html>
    """


@app.get("/Banco_de_dados_SdL_AI") # me leva para a pagina de usuarios (definida pela funcao usuarios)

def Banco_de_dados_SdL_AI(): #retorna a lista de usuários
    cursor.execute("SELECT * FROM dados") #devolve todos os usuários

    dados = cursor.fetchall()

    return dados