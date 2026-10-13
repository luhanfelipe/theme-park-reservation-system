import uuid

class Reserva:
    def __init__(self, cpf_visitante, nome_atracao, horario, status="Ativa", codigo=None):
        # Gera UUID truncado (8 caracteres) caso não venha do banco de dados
        self.codigo = codigo if codigo else str(uuid.uuid4())[:8].upper()
        self.cpf_visitante = cpf_visitante
        self.nome_atracao = nome_atracao
        self.horario = horario
        self.status = status  # "Ativa", "Concluída", "Cancelada"

    def cancelar(self):
        self.status = "Cancelada"

    def concluir(self):
        self.status = "Concluída"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "cpf_visitante": self.cpf_visitante,
            "nome_atracao": self.nome_atracao,
            "horario": self.horario,
            "status": self.status
        }