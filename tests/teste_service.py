# Arquivo: tests/teste_service.py

from src.services.parque_service import ParqueService


def novo_service():
    """Cria um ParqueService limpo para cada teste, evitando estado compartilhado."""
    return ParqueService()


def nomes_fila(service, nome_atracao):
    """Helper: retorna a fila de uma atração como lista de strings legíveis."""
    atracao = service.atracoes.buscar_por("nome", nome_atracao)
    return [str(v) for v in atracao.fila_virtual.listar_fila()]


print("=== Teste 1: cadastro de visitante ===")
s = novo_service()
msg = s.cadastrar_visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal")
assert msg == "Visitante cadastrado com sucesso!", msg
assert len(s.listar_visitantes()) == 1
assert s.listar_visitantes()[0].cpf == "111"
print("OK:", msg)

print("\n=== Teste 2: cadastro de atração ===")
s = novo_service()
msg = s.cadastrar_atracao("Vendaval Eterno", "Montanha-Russa", 30, 12, "10:00", True)
assert msg == "Atração cadastrada com sucesso!", msg
assert len(s.listar_atracoes()) == 1
assert s.listar_atracoes()[0].nome == "Vendaval Eterno"
assert s.listar_atracoes()[0].tipo == "Montanha-Russa"
assert s.listar_atracoes()[0].fila_virtual is not None
print("OK:", msg)

print("\n=== Teste 3: múltiplos cadastros preservam ordem de inserção ===")
s = novo_service()
s.cadastrar_visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal")
s.cadastrar_visitante("Maria", 35, "222", "02/02/1995", "m@e.com", "Normal")
s.cadastrar_visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP")
nomes = [v.nome for v in s.listar_visitantes()]
assert nomes == ["João", "Maria", "Carlos"], nomes
print("OK:", nomes)

print("\n=== Teste 4: fila com visitante inexistente ===")
s = novo_service()
s.cadastrar_atracao("Montanha-Russa", "Montanha-Russa", 30, 12, "10:00", True)
msg = s.adicionar_visitante_na_fila("999", "Montanha-Russa")
assert msg == "Erro: Visitante não encontrado.", msg
print("OK:", msg)

print("\n=== Teste 5: fila com atração inexistente ===")
s = novo_service()
s.cadastrar_visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal")
msg = s.adicionar_visitante_na_fila("111", "AtracaoInexistente")
assert msg == "Erro: Atração não encontrada.", msg
print("OK:", msg)

print("\n=== Teste 6: bloqueio por idade mínima ===")
s = novo_service()
s.cadastrar_visitante("Ana", 10, "444", "04/04/2016", "a@e.com", "Normal")
s.cadastrar_atracao("Montanha-Russa", "Montanha-Russa", 30, 14, "10:00", True)
msg = s.adicionar_visitante_na_fila("444", "Montanha-Russa")
assert msg == "Erro: Ana não tem a idade mínima para Montanha-Russa.", msg
assert nomes_fila(s, "Montanha-Russa") == []
print("OK:", msg)

print("\n=== Teste 7: entrada válida na fila ===")
s = novo_service()
s.cadastrar_visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal")
s.cadastrar_atracao("Montanha-Russa", "Montanha-Russa", 30, 14, "10:00", True)
msg = s.adicionar_visitante_na_fila("111", "Montanha-Russa")
assert msg == "Sucesso: João entrou na fila para Montanha-Russa!", msg
assert nomes_fila(s, "Montanha-Russa") == ["João (Normal)"]
print("OK:", msg)

print("\n=== Teste 8: prioridade — VIP passa na frente de Normal ===")
s = novo_service()
s.cadastrar_visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal")
s.cadastrar_visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP")
s.cadastrar_atracao("Montanha-Russa", "Montanha-Russa", 30, 14, "10:00", True)
s.adicionar_visitante_na_fila("111", "Montanha-Russa")
s.adicionar_visitante_na_fila("333", "Montanha-Russa")
assert nomes_fila(s, "Montanha-Russa") == ["Carlos (VIP)", "João (Normal)"]
print("OK:", nomes_fila(s, "Montanha-Russa"))

print("\n=== Teste 9: atração SEM prioridade — respeita ordem de chegada ===")
s = novo_service()
s.cadastrar_visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal")
s.cadastrar_visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP")
s.cadastrar_atracao("Carrossel", "Carrossel", 10, 0, "10:00", False)
s.adicionar_visitante_na_fila("111", "Carrossel")
s.adicionar_visitante_na_fila("333", "Carrossel")
assert nomes_fila(s, "Carrossel") == ["João (Normal)", "Carlos (VIP)"]
print("OK:", nomes_fila(s, "Carrossel"))

print("\n=== Teste 10: idade em string (como a GUI pode passar) ===")
s = novo_service()
s.cadastrar_visitante("Bia", "30", "555", "05/05/1994", "b@e.com", "Anual")
s.cadastrar_atracao("Roda-Gigante", "Roda-Gigante", 20, 10, "11:00", True)
msg = s.adicionar_visitante_na_fila("555", "Roda-Gigante")
assert msg == "Sucesso: Bia entrou na fila para Roda-Gigante!", msg
print("OK:", msg)

print("\n=== Teste 11: tipo da atração é armazenado ===")
s = novo_service()
s.cadastrar_atracao("Vendaval Eterno", "Montanha-Russa", 30, 14, "10:00", True)
a = s.listar_atracoes()[0]
assert a.nome == "Vendaval Eterno", a.nome
assert a.tipo == "Montanha-Russa", a.tipo
print("OK:", a.nome, "/", a.tipo)

print("\nTodos os testes do ParqueService passaram!")
