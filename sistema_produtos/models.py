import json
import os

class Produto:
    # representa o esqueleto da classe de produto
    def __init__(self, nome, codigo, quantidade, preco):
        self.nome = nome              # nome do produto
        self.codigo = codigo          # código único do produto
        self.quantidade = quantidade  # quantidade em estoque
        self.preco = preco            # preço do produto

    def __repr__(self):
        # representação do produto como string (útil para debug)
        return f"Produto(nome={self.nome}, codigo={self.codigo}, quantidade={self.quantidade}, preco={self.preco})"

    # transforma Produto em dicionário (para salvar no JSON)
    def to_dict(self):
        return {
            "nome": self.nome,
            "codigo": self.codigo,
            "quantidade": self.quantidade, 
            "preco": self.preco   
        }

    # cria Produto a partir de um dicionário (quando carregar do JSON)
    @staticmethod
    def from_dict(dados):
        return Produto(
            dados["nome"],       #nome no arquivo json
            dados["codigo"],     #codigo no arquivo json
            dados["quantidade"], #quantidade no arquivo json
            dados["preco"]       #preço no arquivo json
        )

    # diminui a quantidade em estoque
    def diminuir_estoque(self, quantidade):
        if quantidade > 0 and quantidade <= self.quantidade:
            self.quantidade -= quantidade
        elif quantidade <= 0:
            raise ValueError("A quantidade a ser diminuída deve ser positiva.")
        else:
            raise ValueError("Quantidade insuficiente em estoque.")

    # aumenta a quantidade em estoque
    def aumentar_estoque(self, quantidade):
        if quantidade > 0:
            self.quantidade += quantidade
        else:
            raise ValueError("A quantidade a ser aumentada deve ser positiva.")

    # verifica o estado do estoque
    def verificar_estoque(self):
        return "Produto em estoque" if self.quantidade >= 5 else "Produto em falta"


class SistemaProdutos:
    # representa o sistema de gerenciamento de produtos
    ARQUIVO_JSON = "produtos.json"  # arquivo usado para salvar os dados

    def __init__(self):
        self.produtos = []     # chama a variavel produtos para salvar no json 
        self.carregar_dados()  # carrega os dados do JSON na inicialização

    # ---------------- PERSISTÊNCIA ----------------
    def salvar_dados(self):
        """Salva os produtos no arquivo JSON"""
        with open(self.ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.produtos], f, indent=4, ensure_ascii=False)

    def carregar_dados(self):
        """Carrega os produtos do arquivo JSON"""
        if os.path.exists(self.ARQUIVO_JSON): 
            with open(self.ARQUIVO_JSON, "r", encoding="utf-8") as f:
                try:
                    dados = json.load(f)
                    self.produtos = [Produto.from_dict(d) for d in dados]
                except json.JSONDecodeError:
                    self.produtos = []  # caso o JSON esteja vazio ou corrompido

    # ---------------- CRUD ----------------
    def cadastrar_produto(self, nome, codigo, quantidade, preco):
        # verifica se o código já existe
        for p in self.produtos:
            if p.codigo == codigo:
                raise ValueError(f"Produto com código {codigo} já existe!")
        produto = Produto(nome, codigo, quantidade, preco)
        self.produtos.append(produto)
        self.salvar_dados()
        return f"Produto {codigo}, {nome} cadastrado com sucesso!"

    def remover_produto(self, codigo):
        for p in self.produtos:
            if p.codigo == codigo:
                self.produtos.remove(p)
                self.salvar_dados()
                return f"Produto {codigo} removido com sucesso!"
        raise ValueError("Produto não encontrado.")

    def buscar_produto(self, codigo):
        for p in self.produtos:
            if p.codigo == codigo:
                return p
        return None

    def listar_produtos(self):
        return self.produtos

    def editar_produto(self, codigo, nome=None, quantidade=None, preco=None):
        produto = self.buscar_produto(codigo)
        if not produto:
            raise ValueError("Produto não encontrado.")

        if nome:
            produto.nome = nome
        if quantidade is not None:
            produto.quantidade = quantidade
        if preco is not None:
            produto.preco = preco

        self.salvar_dados()
        return f"Produto {codigo} atualizado com sucesso!"
