# Arquivo: tests/teste_fila_prioridade.py

from src.models.visitante import Visitante
from src.structures.fila_prioridade import FilaPrioridade

# 1. Criando os visitantes
v1 = Visitante("João", 22, "111", "01/01/2000", "joao@email.com", "Normal")
v2 = Visitante("Maria", 35,  "222", "02/02/1995", "maria@email.com", "Normal")
v3 = Visitante("Carlos (VIP)", 54,  "333", "03/03/1990", "carlos@email.com", "VIP")
v4 = Visitante("Ana", 13, "444", "04/04/2005", "ana@email.com", "Normal")
v5 = Visitante("Roberto (VIP)", 14, "555", "05/05/1985", "roberto@email.com", "VIP")

# 2. Criando a Fila de uma Montanha-Russa (que aceita prioridade)
fila_montanha_russa = FilaPrioridade()

# 3. Simulando a chegada na fila
print("--- Chegada na Fila ---")
fila_montanha_russa.enfileirar(v1, atracao_aceita_prioridade=True)
fila_montanha_russa.enfileirar(v2, atracao_aceita_prioridade=True)
print("Fila atual:", fila_montanha_russa.listar_fila()) 
# Esperado: João (Normal), Maria (Normal)

print("\n--- Chegou um VIP! ---")
fila_montanha_russa.enfileirar(v3, atracao_aceita_prioridade=True)
print("Fila atual:", fila_montanha_russa.listar_fila()) 
# Esperado: Carlos (VIP), João (Normal), Maria (Normal) - O VIP tomou a frente!

print("\n--- Chegou mais gente ---")
fila_montanha_russa.enfileirar(v4, atracao_aceita_prioridade=True) # Ana (Normal)
fila_montanha_russa.enfileirar(v5, atracao_aceita_prioridade=True) # Roberto (VIP)
print("Fila atual:", fila_montanha_russa.listar_fila()) 
# Esperado: Carlos (VIP), Roberto (VIP), João (Normal), Maria (Normal), Ana (Normal)

print("\n--- Liberando a catraca do brinquedo (Desenfileirando) ---")
atendido = fila_montanha_russa.desenfileirar()
print(f"Entrou no brinquedo: {atendido.nome}")
print("Fila após o embarque:", fila_montanha_russa.listar_fila())