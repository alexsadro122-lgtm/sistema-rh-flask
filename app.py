# Importação das bibliotecas
from flask import Flask, flash, redirect, render_template, request, session
import sqlite3

# Inicialização do Flask
app = Flask(__name__)
app.secret_key = "123456"

# Chave secreta para mensagens flash
app.secret_key = "123456"

# Função responsável por criar o banco de dados
def criar_banco():
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()
    
    # Criação da tabela de funcionários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        
        )
    ''')
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
        ('Admin', 'admin@example.com', 'admin123')
    )

    conexao.commit()
    conexao.close()

# Rota principal do sistema
@app.route("/")
def home():

    if "usuario" not in session:
        return redirect("/login")

    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()

    total_funcionarios = len(funcionarios)

    cursor.execute(
        "SELECT COUNT(DISTINCT cargo) FROM funcionarios"
    )

    total_cargos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT nome FROM funcionarios
        ORDER BY id DESC
        LIMIT 1
    """)

    ultimo_funcionario = cursor.fetchone()

    if ultimo_funcionario:
        ultimo_funcionario = ultimo_funcionario[0]
    else:
        ultimo_funcionario = "Nenhum"

    conexao.close()

    return render_template(
        "index.html",
        funcionarios=funcionarios,
        total_funcionarios=total_funcionarios,
        total_cargos=total_cargos,
        ultimo_funcionario=ultimo_funcionario
    )


# ROTA LOGIN
@app.route("/login")
def login():
    return render_template("login.html")

# Rota responsável por cadastrar funcionários
@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"]
    email = request.form["email"]
    cargo = request.form["cargo"]

    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()

    # Insere funcionário no banco
    cursor.execute(
        "INSERT INTO funcionarios (nome, email, cargo) VALUES (?, ?, ?)",
        (nome, email, cargo)
    )

    conexao.commit()
    conexao.close()

    flash("Funcionário cadastrado com sucesso!")

    return redirect("/")


# Rota para deletar funcionários
@app.route("/deletar/<int:id>", methods=["POST"])
def deletar(id):
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()

    # Remove funcionário pelo ID
    cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()

    flash("Funcionário removidocom sucesso!")

    return redirect("/")

# Rota para editar funcionários
@app.route("/editar/<int:id>")
def editar(id):
    
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM funcionarios WHERE id = ?",
         (id,)
    )
    
    funcionario = cursor.fetchone()

    conexao.close()

    return render_template("editar.html", funcionario=funcionario
)

# Rota para atualizar funcionários
@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    nome = request.form["nome"]
    email = request.form["email"]
    cargo = request.form["cargo"]

    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()

    cursor.execute(
        """ UPDATE funcionarios
        SET nome = ?, email = ?, cargo = ?
        WHERE id = ?""",
        (nome, email, cargo, id)
    )

    conexao.commit()
    conexao.close()

    flash("Funcionário atualizado com sucesso!")
    
    return redirect("/")

# Rota para autenticar usuários
@app.route("/autenticar", methods=["POST"])
def autenticar():
    email = request.form["email"]
    senha = request.form["senha"]

    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha)
    )

    usuario = cursor.fetchone()

    conexao.close()

    if usuario:
        session["usuario"] = usuario[1]  # Armazena o nome do usuário na sessão
        flash("Login realizado com sucesso!")
        return redirect("/")
    else:
        flash("Email ou senha inválidos!")
        return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("usuario", None)  # Remove o usuário da sessão
    flash("Logout realizado com sucesso!")
    return redirect("/login")

# Cria o banco ao iniciar o sistema
criar_banco()


# Executa o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
