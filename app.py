from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cadastro_integrador"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/realizar-sorteio")
def realizar_sorteio():
    conn = conectar()
    cursor = conn.cursor(dictionary=True) 

    sql = "SELECT id, primeiro_nome, sobrenome FROM usuarios ORDER BY RAND() LIMIT 1"
    
    cursor.execute(sql)
    ganhador = cursor.fetchone() 

    cursor.close()
    conn.close()

    if ganhador:
        return render_template("sorteio.html", ganhador=ganhador)
    else:
        return "Nenhum participante encontrado para o sorteio. <a href='/'>Voltar</a>"

@app.route("/salvar", methods=["POST"])
def salvar():
    primeiro_nome = request.form["primeiro_nome"]
    sobrenome = request.form["sobrenome"]
    data_nascimento = request.form["data_nascimento"]
    tipo_usuario = request.form["tipo_usuario"]

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO usuarios 
        (primeiro_nome, sobrenome, tipo_usuario, data_nascimento) 
        VALUES (%s, %s, %s, %s)
    """
    valores = (primeiro_nome, sobrenome, tipo_usuario, data_nascimento)

    cursor.execute(sql, valores)
    conn.commit()
    
    sorteio_id = cursor.lastrowid 

    cursor.close()
    conn.close()

    return render_template("sucesso.html", numero_sorteio=sorteio_id)


if __name__ == "__main__":
    app.run(debug=True)
 
 
