class Carteira:
    def __init__(self,codigo,senha,cliente,tokens):
        self.codigo = codigo
        self.senha = senha
        self.cliente = cliente
        self.tokens = tokens
    def getCodigo(self):
        return self.codigo
    def getCliente(self):
        return self.cliente 
    def totalTokens(self):
        return len(self.tokens)