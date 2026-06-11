class Produto:
    def __init__(self, nome, preco, descricao):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
    def getNome(self):
        return self.nome
    def getDescricao(self):
        return self.descricao
    def getPreco(self):
        return self.preco