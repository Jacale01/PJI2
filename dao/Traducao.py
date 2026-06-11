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


# Exemplos de teste
if __name__ == "__main__":
    print("=== Testes da função calcularTokensGerados ===\n")
    
    # Teste 1: Energia 10 (10 * 0.1 = 1)
    t1 = Traducao(10, 1)
    resultado1 = t1.calcularTokensGerados()
    print(f"Teste 1 - Energia: 10")
    print(f"Tokens gerados: {resultado1}")
    print(f"Tipo: {type(resultado1).__name__}")
    print(f"Sucesso: {isinstance(resultado1, int) and resultado1 == 1}\n")
    
    # Teste 2: Energia 100 (100 * 0.1 = 10)
    t2 = Traducao(100, 2)
    resultado2 = t2.calcularTokensGerados()
    print(f"Teste 2 - Energia: 100")
    print(f"Tokens gerados: {resultado2}")
    print(f"Tipo: {type(resultado2).__name__}")
    print(f"Sucesso: {isinstance(resultado2, int) and resultado2 == 10}\n")
    
    # Teste 3: Energia 255 (255 * 0.1 = 25.5, retorna 25)
    t3 = Traducao(255, 3)
    resultado3 = t3.calcularTokensGerados()
    print(f"Teste 3 - Energia: 255")
    print(f"Tokens gerados: {resultado3}")
    print(f"Tipo: {type(resultado3).__name__}")
    print(f"Sucesso: {isinstance(resultado3, int) and resultado3 == 25}\n")
    
    # Teste 4: Energia 5 (5 * 0.1 = 0.5, retorna 0)
    t4 = Traducao(5, 4)
    resultado4 = t4.calcularTokensGerados()
    print(f"Teste 4 - Energia: 5")
    print(f"Tokens gerados: {resultado4}")
    print(f"Tipo: {type(resultado4).__name__}")
    print(f"Sucesso: {isinstance(resultado4, int) and resultado4 == 0}\n")
    
    # Teste 5: Energia 1000 (1000 * 0.1 = 100)
    t5 = Traducao(1000, 5)
    resultado5 = t5.calcularTokensGerados()
    print(f"Teste 5 - Energia: 1000")
    print(f"Tokens gerados: {resultado5}")
    print(f"Tipo: {type(resultado5).__name__}")
    print(f"Sucesso: {isinstance(resultado5, int) and resultado5 == 100}")