import pytest
from src.services.parque_service import ParqueService
from src.structures.lista_encadeada import ListaEncadeada
from src.database import db

class DummyVisitante:
    def __init__(self, nome, cpf, tipo_passe):
        self.nome = nome
        self.cpf = cpf
        self.tipo_passe = tipo_passe
        self.idade = 20

class DummyFilaVirtual:
    def __init__(self):
        self.fila = []
    def enfileirar(self, visitante, prioridade=False):
        self.fila.append(visitante)

class DummyAtracao:
    def __init__(self, nome):
        self.nome = nome
        self.aceita_prioridade = False
        self.idade_minima = 0
        self.fila_virtual = DummyFilaVirtual()

def setup_service():
    service = ParqueService()
    
    # Reinicia as listas encadeadas para o ambiente de teste
    service.reservas = ListaEncadeada()
    service.visitantes = ListaEncadeada()
    service.atracoes = ListaEncadeada()

    # Inserindo visitantes de teste
    service.visitantes.inserir(DummyVisitante("João", "11111111111", "Normal"))
    service.visitantes.inserir(DummyVisitante("Maria", "22222222222", "Passe Anual"))
    service.visitantes.inserir(DummyVisitante("Alan", "33333333333", "VIP"))

    # Inserindo atrações de teste
    service.atracoes.inserir(DummyAtracao("Montanha Russa"))
    service.atracoes.inserir(DummyAtracao("Roda Gigante"))
    service.atracoes.inserir(DummyAtracao("Carrossel"))
    service.atracoes.inserir(DummyAtracao("Simulador"))

    return service

def test_criacao_reserva_valida():
    service = setup_service()
    sucesso, res = service.criar_reserva("11111111111", "Montanha Russa", "14:00")
    assert sucesso is True
    assert res.cpf_visitante == "11111111111"
    assert res.status == "Ativa"

def test_bloqueio_por_limite_passe():
    service = setup_service()
    # Normal: limite 1
    s1, _ = service.criar_reserva("11111111111", "Montanha Russa", "14:00")
    s2, msg2 = service.criar_reserva("11111111111", "Roda Gigante", "15:00")
    assert s1 is True
    assert s2 is False
    assert "Limite" in msg2

def test_bloqueio_por_conflito_horario():
    service = setup_service()
    s1, _ = service.criar_reserva("33333333333", "Montanha Russa", "14:00")
    s2, msg2 = service.criar_reserva("33333333333", "Roda Gigante", "14:00")
    assert s1 is True
    assert s2 is False
    assert "mesmo horário" in msg2

def test_cancelamento_reserva():
    service = setup_service()
    sucesso, res = service.criar_reserva("11111111111", "Montanha Russa", "14:00")
    
    # Admin não pode cancelar
    ok_admin, _ = service.cancelar_reserva(res.codigo, e_visitante=False)
    assert ok_admin is False

    # Visitante cancela com sucesso
    ok_vis, _ = service.cancelar_reserva(res.codigo, e_visitante=True)
    assert ok_vis is True
    assert res.status == "Cancelada"

def test_persistencia_sqlite():
    service = setup_service()
    
    # Criar reserva que será salva no SQLite
    sucesso, res = service.criar_reserva("11111111111", "Montanha Russa", "14:00")
    assert sucesso is True
    
    # Recarregar diretamente do banco de dados SQLite
    reservas_banco = db.carregar_reservas()
    codigos_banco = [r.codigo for r in reservas_banco]
    
    # Verifica se o código da reserva criada está no banco
    assert res.codigo in codigos_banco