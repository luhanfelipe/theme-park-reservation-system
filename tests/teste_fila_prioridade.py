# Arquivo: tests/teste_fila_prioridade.py

from src.models.visitante import Visitante
from src.structures.fila_prioridade import FilaPrioridade


def nomes(fila):
    """Helper: transforma a fila numa lista de strings legíveis para comparar."""
    return [str(v) for v in fila.listar_fila()]


print("=== Teste 1: fila vazia + Normal ===")
f = FilaPrioridade()
f.enfileirar(Visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal"))
assert nomes(f) == ["João (Normal)"], nomes(f)
print("OK:", nomes(f))

print("\n=== Teste 2: [Normal, Normal] + VIP ===")
f = FilaPrioridade()
f.enfileirar(Visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal"))
f.enfileirar(Visitante("Maria", 35, "222", "02/02/1995", "m@e.com", "Normal"))
f.enfileirar(Visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP"))
assert nomes(f) == ["Carlos (VIP)", "João (Normal)", "Maria (Normal)"], nomes(f)
print("OK:", nomes(f))

print("\n=== Teste 3: [VIP] + Anual ===")
f = FilaPrioridade()
f.enfileirar(Visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP"))
f.enfileirar(Visitante("Bia", 30, "444", "04/04/1994", "b@e.com", "Anual"))
assert nomes(f) == ["Carlos (VIP)", "Bia (Anual)"], nomes(f)
print("OK:", nomes(f))

print("\n=== Teste 4: [VIP, Anual] + Normal ===")
f = FilaPrioridade()
f.enfileirar(Visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP"))
f.enfileirar(Visitante("Bia", 30, "444", "04/04/1994", "b@e.com", "Anual"))
f.enfileirar(Visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal"))
assert nomes(f) == ["Carlos (VIP)", "Bia (Anual)", "João (Normal)"], nomes(f)
print("OK:", nomes(f))

print("\n=== Teste 5: [VIP, Normal] + Anual (entra no meio) ===")
f = FilaPrioridade()
f.enfileirar(Visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP"))
f.enfileirar(Visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal"))
f.enfileirar(Visitante("Bia", 30, "444", "04/04/1994", "b@e.com", "Anual"))
assert nomes(f) == ["Carlos (VIP)", "Bia (Anual)", "João (Normal)"], nomes(f)
print("OK:", nomes(f))

print("\n=== Teste 6: dois VIPs (empate preserva chegada) ===")
f = FilaPrioridade()
f.enfileirar(Visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP"))
f.enfileirar(Visitante("Roberto", 14, "555", "05/05/1985", "r@e.com", "VIP"))
assert nomes(f) == ["Carlos (VIP)", "Roberto (VIP)"], nomes(f)
print("OK:", nomes(f))

print("\n=== Teste 7: atração NÃO aceita prioridade ===")
f = FilaPrioridade()
f.enfileirar(Visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal"), atracao_aceita_prioridade=False)
f.enfileirar(Visitante("Carlos", 54, "333", "03/03/1990", "c@e.com", "VIP"), atracao_aceita_prioridade=False)
f.enfileirar(Visitante("Bia", 30, "444", "04/04/1994", "b@e.com", "Anual"), atracao_aceita_prioridade=False)
assert nomes(f) == ["João (Normal)", "Carlos (VIP)", "Bia (Anual)"], nomes(f)
print("OK:", nomes(f))

print("\n=== Teste 8: listar_fila em fila vazia ===")
f = FilaPrioridade()
assert f.listar_fila() == [], f.listar_fila()
print("OK:", f.listar_fila())

print("\nTodos os testes da fila de prioridade passaram!")
