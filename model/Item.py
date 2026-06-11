class Item:
    def __init__(self, quantidade, produto):
        self.quantidade = quantidade
        self.produto = produto
    def getSubValor(self):
        return self.produto.getPreco() * self.quantidade
    def getQuantidade(self):
        return self.quantidade
    def getProduto(self):
        return self.produto