# Arquivo: tests/teste_db.py
# Testa o módulo de persistência de forma isolada, sem tocar no banco real.

import os
import importlib

# Força o db.py a usar um banco temporário antes de importar
os.environ["PARQUE_DB_TESTE"] = "1"

from src.database import db
from src.models.visitante import Visitante
from src.models.atracao import Atracao


# Redireciona pro banco de teste (não mexe no data/parque.db real)
db.CAMINHO_BANCO = os.path.join("data", "teste.db")

# Limpa qualquer resíduo de execuções anteriores
if os.path.exists(db.CAMINHO_BANCO):
    os.remove(db.CAMINHO_BANCO)


print("=== Teste 1: criar tabelas ===")
db.criar_tabelas()
assert os.path.exists(db.CAMINHO_BANCO), "Banco não foi criado"
print("OK: banco criado em", db.CAMINHO_BANCO)

print("\n=== Teste 2: salvar e carregar visitante ===")
v = Visitante("João", 22, "111", "01/01/2000", "j@e.com", "Normal", "1234-5678")
db.salvar_visitante(v)
carregados = db.carregar_visitantes()
assert len(carregados) == 1, carregados
assert carregados[0].nome == "João"
assert carregados[0].cpf == "111"
assert carregados[0].tipo_passe == "Normal"
assert carregados[0].cartao == "1234-5678"
print("OK:", carregados[0].nome, "/", carregados[0].cpf)

print("\n=== Teste 3: salvar e carregar atração ===")
a = Atracao("Vendaval Eterno", "Montanha-Russa", 30, 14, "10:00", True)
db.salvar_atracao(a)
carregadas = db.carregar_atracoes()
assert len(carregadas) == 1, carregadas
assert carregadas[0].nome == "Vendaval Eterno"
assert carregadas[0].tipo == "Montanha-Russa"
assert carregadas[0].capacidade == 30
assert carregadas[0].idade_minima == 14
assert carregadas[0].aceita_prioridade is True
print("OK:", carregadas[0].nome, "/", carregadas[0].tipo)

print("\n=== Teste 4: duplicidade de CPF é ignorada ===")
db.salvar_visitante(Visitante("Outro João", 30, "111", "01/01/1994", "x@e.com", "VIP"))
carregados = db.carregar_visitantes()
assert len(carregados) == 1, carregados
assert carregados[0].nome == "João", carregados[0].nome
print("OK: duplicidade ignorada")

print("\n=== Teste 5: duplicidade de nome de atração é ignorada ===")
db.salvar_atracao(Atracao("Vendaval Eterno", "Simulador", 20, 10, "11:00", False))
carregadas = db.carregar_atracoes()
assert len(carregadas) == 1, carregadas
assert carregadas[0].tipo == "Montanha-Russa", carregadas[0].tipo
print("OK: duplicidade ignorada")

print("\n=== Teste 6: aceita_prioridade False é preservado ===")
db.salvar_atracao(Atracao("Carrossel", "Carrossel", 10, 0, "10:00", False))
carregadas = db.carregar_atracoes()
carrossel = [a for a in carregadas if a.nome == "Carrossel"][0]
assert carrossel.aceita_prioridade is False
print("OK: Carrossel aceita_prioridade =", carrossel.aceita_prioridade)

# Limpeza final
os.remove(db.CAMINHO_BANCO)
print("\nBanco de teste removido. Todos os testes de persistência passaram!")
