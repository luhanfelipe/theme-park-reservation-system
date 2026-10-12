# Arquivo: tests/seed_thorpe_park.py
# Popula o banco real (data/parque.db) com as atrações reais do Thorpe Park (UK).
# Uso: .venv/bin/python -m tests.seed_thorpe_park

from src.database import db


# Dados reais do Thorpe Park (Inglaterra)
# Fonte: site oficial e materiais do parque.
# Formato: (nome, tipo, capacidade, idade_minima, horario, aceita_prioridade)
ATRACOES_THORPE_PARK = [
    ("SAW - The Ride", "Montanha-Russa", 8, 13, "10:00-18:00", True),
    ("The Walking Dead: The Ride", "Simulador", 8, 13, "10:00-18:00", True),
    ("Ghost Train", "Teatro", 8, 13, "12:00-18:00", True),
    ("The Swarm", "Montanha-Russa", 24, 13, "10:00-18:00", True),
    ("Hyperia", "Montanha-Russa", 24, 13, "10:00-18:00", True),
    ("Stealth", "Montanha-Russa", 24, 13, "10:00-18:00", True),
    ("Colossus", "Montanha-Russa", 24, 13, "10:00-18:00", True),
    ("Nemesis Inferno", "Montanha-Russa", 24, 13, "10:00-18:00", True),
]


def popular():
    """Garante as tabelas e insere as atrações do Thorpe Park no banco real."""
    db.criar_tabelas()

    print(f"Inserindo {len(ATRACOES_THORPE_PARK)} atrações do Thorpe Park...")
    for nome, tipo, capacidade, idade_minima, horario, aceita in ATRACOES_THORPE_PARK:
        # Cria um objeto Atracao só pra chamar salvar_atracao
        from src.models.atracao import Atracao
        atracao = Atracao(nome, tipo, capacidade, idade_minima, horario, aceita)
        db.salvar_atracao(atracao)
        print(f"  ✓ {nome} ({tipo})")

    # Mostra o resultado final
    print("\nAtrações no banco agora:")
    for a in db.carregar_atracoes():
        print(f"  - {a.nome} ({a.tipo})")


if __name__ == "__main__":
    popular()
    print("\nSeed concluído. Rode .venv/bin/python -m src.main para ver na GUI.")
