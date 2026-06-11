class Cliente:
    def __init__(self, nome,telefone,email,id, cpf,endereco):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.id = id
        self.cpf = cpf
        self.endereco = endereco
    def getNome(self):
        return self.nome
    def getCpf(self):
        return self.cpf
    def getTelefone(self):
        return self.telefone
    def getEmail(self):
        return self.email
    def getId(self):
        return self.id
    def getEndereco(self):
        return self.endereco