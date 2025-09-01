class Login:
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.__senha = senha  # senha privada

    def __str__(self):
        return f"Usuário: {self.usuario}"

    def validar_senha(self, senha_digitada):
        return self.__senha == senha_digitada 