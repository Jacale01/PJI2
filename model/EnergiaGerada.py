class EnergiGerada:
    def __init__(self, quantidade, periodo, cliente):
        self.quantidade = quantidade
        self.periodo = periodo
        self.cliente = cliente
    def getCliente(self):
        return self.cliente
    def getQuantidade(self):
        return self.quantidade
    def getPeriodo(self):
        return self.periodo