from fastapi import FastAPI #importa FastAPI pra criar a API 
import psycopg2 # conexão com o banco de dados online


app = FastAPI() #cria a API

conexao = psycopg2.connect("postgresql://neondb_owner:npg_Np2OZbvC7EmA@ep-divine-wildflower-actmdwf8-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
# cria a conexão com o meu projeto do Neon (conexao com SQL, https, etc etc etc)

cursor = conexao.cursor() #envia comandos SQL (linguagem do banco de dados)




cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
            id SERIAL PRIMARY KEY,
            pergunta TEXT,
            resposta TEXT
            )
""") #cria uma tabela de usuários com SQL 


cursor.execute("""
INSERT INTO usuarios (pergunta, resposta)
VALUES ('Quem é o líder do BTS?','Namjoonie')""") #adiciona uma linha de pergunta e resposta








@app.get("/") # página inicial, me leva à função inicio

def inicio(): #retorna a letra de Holligan na página inicial
    introducao = "hahahahahahahahahahahaha HOlligan"
    return introducao

@app.get("/usuarios") # me leva para a pagina de usuarios (definida pela funcao usuarios)

def usuarios(): #retorna a lista de usuários
    cursor.execute("SELECT * FROM usuarios") #devolve todos os usuários

    dados = cursor.fetchall()

    return dados