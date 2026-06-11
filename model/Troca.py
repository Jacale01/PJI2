class Troca:
    def __init__(self, id, data, cliente, item):
        self.id = id
        self.data = data
        self.cliente = cliente
        self.item = item
    def getId(self):
        return self.id
    def getData(self):
        return self.data
    def getCliente(self):
        return self.cliente
    def getItem(self):
        return self.item
    def getValorTotal(self):
        valorTotal = 0
        for item in self.item:
            valorTotal += item.getSubValor()
        return valorTotal