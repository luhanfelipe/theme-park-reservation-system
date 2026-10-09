from src.structures.fila_prioridade import FilaPrioridade

class Atracao:
    def __init__(self, nome, capacidade, idade_minima, horario, aceita_prioridade):
        self.nome = nome
        self.capacidade = capacidade
        self.idade_minima = idade_minima
        self.horario = horario
        self.aceita_prioridade = aceita_prioridade
        self.fila_virtual = FilaPrioridade()