class Visitante:
    def __init__(self, nome, idade, cpf, data_nascimento, email, tipo_passe):
        self.nome = nome
        self.idade = idade
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.tipo_passe = tipo_passe

    def __str__(self):
        return f"{self.nome} ({self.tipo_passe})"