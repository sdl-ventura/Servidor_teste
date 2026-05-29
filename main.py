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

cursor.execute("DELETE FROM dados")

with open("dados.csv", newline="", encoding="utf-8") as arquivo:

    leitor = csv.reader(arquivo)

    next(leitor)

    for linha in leitor:

        tema = linha[1]
        pergunta = linha[2]
        resposta = linha[3]
        fonte = linha[4]


        cursor.execute(
            """
            INSERT INTO dados (pergunta, resposta)
            VALUES (%s, %s)
            """,
            (tema, pergunta, resposta, fonte)
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
                src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXRqYW1maGU5YXVleW8zOGl3ejI3bzkwZWhxaDRxZ2hqdjZsNWQzMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O0VBge9U7f8j21UqNj/giphy.gif"
                width="800"

            </p>

            </p>

            <a href="/Banco_de_dados_SdL_IA">
                Ver Banco de Dados
            </a>

        </body>
    </html>
    """


@app.get("/Banco_de_dados_SdL_IA") # me leva para a pagina de usuarios (definida pela funcao usuarios)

def Banco_de_dados_SdL_IA(): #retorna a lista de usuários
    cursor.execute("SELECT * FROM dados") #devolve todos os usuários

    dados = cursor.fetchall()

    linhas = ""
    # deixando a tabela bonita... 
    for info in dados:
        linhas += f"""
        <tr>
            <td>{info[0]}</td>
            <td>{info[1]}</td>
            <td>{info[2]}</td>
            <td>{info[3]}</td>
            <td>{info[4]}</td>
        </tr>
        """       


    return f"""
    <html>
        <head>
            <title> Q&A Mecânica Quântica para treinar IA</title>

            <style>

            body {{
                background-color: #0f0f0f;
                color: white;
                font-family: Arial;
                padding: 40px
            }}
            h1 {{
                text-align: center;
                color: black;
            }}

            table{{
                width: 80%;
                margin: auto;
                border-collapse: collapse;
                background-color: #1a1a1a;
            }}

            th, td {{
                border: 1px solid purple;
                padding: 12px;
                text-align: center;
            }}

            th {{
                background-color: #c8a2c8;
                color: white;
            }}

            tr:hover {{
                background-color: #333333;
            }}

            a {{
                color: purple;
                text-decoration: none;
            }}

            </style>

        </head>

        <body>
            <h1> Dados para alimentar IA SdL</h1>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Tema</th>
                    <th>Pergunta</th>
                    <th>Resposta</th>
                    <th>Fonte (se diferente dos livros citados)</th>
                </tr>

                {linhas}
            </table>

            <br><br>


            <div style="text-align:center;">
                <a href="/">Voltar</a>
            </div>

        </body>

    </html>
    """ 
