class Traducao:
    def __init__(self, energiaGerada, id):
        self.energiaGerada = energiaGerada
        self.id = id
    def getId(self):
        return self.id
    def getEnergiaGerada(self):
        return self.energiaGerada
    def calcularTokensGerados(self):
        return int(self.energiaGerada * 0.1)