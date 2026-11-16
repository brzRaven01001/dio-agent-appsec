"""
Loja de laboratorio - ambiente LOCAL para testar o modulo avancado de SQL Injection.
"""
import sqlite3
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "lab-secret"
DB = "loja.db"


def conectar():
    return sqlite3.connect(DB)


def init_db():
    conn = conectar()
    cur = conn.cursor()
    cur.executescript(
        """
        DROP TABLE IF EXISTS produtos;
        DROP TABLE IF EXISTS usuarios;
        DROP TABLE IF EXISTS pedidos;
        CREATE TABLE produtos (id INTEGER PRIMARY KEY, nome TEXT, preco REAL, categoria TEXT);
        CREATE TABLE usuarios (id INTEGER PRIMARY KEY, nome TEXT, senha TEXT, email TEXT, perfil TEXT);
        CREATE TABLE pedidos (id INTEGER PRIMARY KEY, usuario TEXT, produto_id INTEGER, total REAL, criado_em TEXT);
        INSERT INTO produtos VALUES (1, 'Teclado Mecanico', 250.0, 'perifericos');
        INSERT INTO produtos VALUES (2, 'Mouse Gamer', 120.0, 'perifericos');
        INSERT INTO produtos VALUES (3, 'Monitor 24', 900.0, 'monitores');
        INSERT INTO usuarios VALUES (1, 'admin', 'Adm!n2024', 'admin@loja.lab', 'admin');
        INSERT INTO usuarios VALUES (2, 'murilo', 'senha123', 'murilo@loja.lab', 'cliente');
        INSERT INTO pedidos VALUES (1, 'murilo', 1, 250.0, '2026-11-01');
        INSERT INTO pedidos VALUES (2, 'murilo', 3, 900.0, '2026-11-10');
        """
    )
    conn.commit()
    conn.close()


@app.route("/produto")
def produto():
    pid = request.args.get("id", "1")
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, nome, preco FROM produtos WHERE id = " + pid)
        linhas = cur.fetchall()
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.close()
    return jsonify(linhas)


@app.route("/busca")
def busca():
    termo = request.args.get("q", "")
    conn = conectar()
    cur = conn.cursor()
    sql = f"SELECT id, nome, preco FROM produtos WHERE nome LIKE '%{termo}%' AND categoria = 'perifericos'"
    cur.execute(sql)
    resultado = cur.fetchall()
    conn.close()
    return jsonify(resultado)


@app.route("/pedidos")
def pedidos():
    usuario = request.args.get("usuario", "murilo")
    ordem = request.args.get("ordem", "criado_em")
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, produto_id, total, criado_em FROM pedidos WHERE usuario = ? ORDER BY " + ordem, (usuario,))
    resultado = cur.fetchall()
    conn.close()
    return jsonify(resultado)


@app.route("/api/usuario-existe")
def usuario_existe():
    nome = request.args.get("nome", "")
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM usuarios WHERE nome = '" + nome + "'")
        existe = cur.fetchone() is not None
    except Exception:
        existe = False
    conn.close()
    return jsonify({"existe": existe})


@app.route("/registro", methods=["POST"])
def registro():
    nome = request.form.get("nome", "").replace("--", "")
    senha = request.form.get("senha", "")
    email = request.form.get("email", "")
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nome, senha, email, perfil) VALUES (?, ?, ?, 'cliente')", (nome, senha, email))
    conn.commit()
    conn.close()
    session["usuario"] = nome
    return jsonify({"ok": True})


@app.route("/perfil")
def perfil():
    nome = session.get("usuario")
    if not nome:
        return jsonify({"erro": "faca login"}), 401
    conn = conectar()
    cur = conn.cursor()
    cur.execute(f"SELECT nome, email, perfil FROM usuarios WHERE nome = '{nome}'")
    dados = cur.fetchone()
    conn.close()
    return jsonify(dados)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=False)