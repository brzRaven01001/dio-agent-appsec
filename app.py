"""
Mini sistema de login - ambiente de LABORATORIO.
Use apenas localmente, para testar o agente de analise de vulnerabilidades.
"""
import sqlite3
from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = "123456"

DB = "usuarios.db"

LOGIN_HTML = """
<h2>Login</h2>
<form method="POST">
  <input name="usuario" placeholder="Usuario"><br>
  <input name="senha" type="password" placeholder="Senha"><br>
  <button type="submit">Entrar</button>
</form>
<p style="color:red">{{ erro }}</p>
"""


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS usuarios ("
        "id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT, perfil TEXT)"
    )
    cur.execute("DELETE FROM usuarios")
    cur.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES ('admin', 'admin123', 'admin')")
    cur.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES ('murilo', 'senha123', 'user')")
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        query = "SELECT * FROM usuarios WHERE usuario = '" + usuario + "' AND senha = '" + senha + "'"
        cur.execute(query)
        user = cur.fetchone()
        conn.close()

        if user:
            session["usuario"] = user[1]
            session["perfil"] = user[3]
            return redirect("/painel")
        erro = "Usuario ou senha invalidos"
    return render_template_string(LOGIN_HTML, erro=erro)


@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/")
    return render_template_string(
        f"<h2>Bem-vindo, {session['usuario']}!</h2><p>Perfil: {session['perfil']}</p>"
    )


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)