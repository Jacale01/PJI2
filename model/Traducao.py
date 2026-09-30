class Traducao:
    def __init__(self, energiaGerada, id):
        self.energiaGerada = energiaGerada
        self.id = id
        self.tokensGerados = self.calcularTokensGerados()
    def getId(self):
        return self.id
    def getEnergiaGerada(self):
        return self.energiaGerada
    def getTokensGerados(self):
        return self.tokensGerados
    def calcularTokensGerados(self):
        return int((self.energiaGerada ** 2)/10000)