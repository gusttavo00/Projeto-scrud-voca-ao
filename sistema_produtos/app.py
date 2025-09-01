from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import SistemaProdutos
from login import Login
import json
import os

app = Flask(__name__)
app.secret_key = "segredo"  # Chave usada para manter a sessão do usuário

# Instância do sistema de produtos
sistema = SistemaProdutos()

# Usuário de teste para login
usuario_admin = Login("admin", "1234")


@app.route("/login", methods=["GET", "POST"]) 
def login():                              

    if request.method == "POST":         
        usuario = request.form["usuario"]  
        senha = request.form["senha"] 

       
        if usuario == usuario_admin.usuario and usuario_admin.validar_senha(senha): 
            session["usuario"] = usuario 
            flash(" Login realizado com sucesso!", "success")
            return redirect(url_for("index")) 
        else:
            flash(" Usuário ou senha inválidos.", "error")
            return redirect(url_for("login"))      
    return render_template("login.html")   


@app.route("/logout")
def logout(): 
    """Finaliza a sessão do usuário e volta para o login"""
    session.pop("usuario", None)
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("login"))


@app.route("/")
def index(): 
    """
    Página inicial (cadastro de produtos).
    Só é acessível para usuários logados.
    """
    if "usuario" in session:   
        return render_template("cadastro_produtos.html")
    return redirect(url_for("login"))


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    """
    Cadastra um novo produto no sistema.
    Dados: nome, código (int), quantidade (int), preço (float).
    """
    if "usuario" not in session:
        return redirect(url_for("login"))

    nome = request.form['nome']
    codigo = int(request.form['codigo'])   # garante que é número no codigo do produto
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])

    # ---------------- VALIDAÇÕES ----------------
    if preco <= 0:
        flash(" O preço deve ser maior que 0.", "error")
        return redirect(url_for('index'))
    if quantidade < 0:
        flash(" A quantidade não pode ser negativa.", "error")
        return redirect(url_for('index'))

    # ---------------- CADASTRO ----------------
    try:
        sistema.cadastrar_produto(nome, codigo, quantidade, preco)
        flash(" Produto cadastrado com sucesso!", "success")
        return redirect(url_for('listar'))
    except ValueError as e:
        flash(f" {str(e)}", "error")
        return redirect(url_for('index'))


@app.route("/produtos")
def listar():
    """
    Lista todos os produtos cadastrados.
    Só acessível para usuários logados.
    """
    if "usuario" not in session:
        return redirect(url_for("login"))
    produtos = sistema.listar_produtos()
    return render_template("lista_produtos.html", produtos=produtos)


@app.route("/remover/<codigo>")
def remover(codigo):
    """
    Remove um produto pelo código.
    """
    if "usuario" not in session:
        return redirect(url_for("login"))

    try:
        sistema.remover_produto(int(codigo))
        flash(" Produto removido com sucesso!", "success")
    except ValueError as e:
        flash(f"{str(e)}", "error")
    return redirect(url_for('listar'))


@app.route("/editar/<codigo>", methods=["GET", "POST"])
def editar(codigo):
    """
    Edita as informações de um produto existente.
    """
    if "usuario" not in session:
        return redirect(url_for("login"))

    produto = sistema.buscar_produto(int(codigo))
    if not produto:
        flash(" Produto não encontrado.", "error")
        return redirect(url_for('listar'))

    if request.method == "POST":
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])

        # Validações de edição
        if preco <= 0:
            flash(" O preço deve ser maior que 0.", "error")
            return redirect(url_for('editar', codigo=codigo))
        if quantidade < 0:
            flash("A quantidade não pode ser negativa.", "error")
            return redirect(url_for('editar', codigo=codigo))

        sistema.editar_produto(produto.codigo, nome, quantidade, preco)
        flash("Produto editado com sucesso!", "success")
        return redirect(url_for('listar'))

    return render_template("editar_produtos.html", produto=produto)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    """
    Executa a aplicação Flask em modo debug.
    """
    app.run(debug=True)
