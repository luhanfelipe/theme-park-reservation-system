# Arquivo: tests/seed_visitantes.py
# Popula o banco real (data/parque.db) com 20 visitantes fictícios.
# Uso: .venv/bin/python -m tests.seed_visitantes

from src.database import db
from src.models.visitante import Visitante


# Formato: (nome, idade, cpf, data_nascimento, email, tipo_passe, cartao)
VISITANTES_SEED = [
    # --- Brasileiros ---
    ("João Pedro Almeida", 28, "11111111111", "15/03/1996", "joao.almeida@email.com", "VIP", "4111-1111-1111-1111"),
    ("Maria Clara Souza", 34, "22222222222", "22/07/1990", "maria.souza@email.com", "Anual", "4222-2222-2222-2222"),
    ("Carlos Eduardo Lima", 45, "33333333333", "10/01/1979", "carlos.lima@email.com", "Normal", ""),
    ("Ana Beatriz Rocha", 22, "44444444444", "05/11/2002", "ana.rocha@email.com", "VIP", "4444-4444-4444-4444"),
    ("Lucas Gabriel Ferreira", 19, "55555555555", "18/09/2005", "lucas.ferreira@email.com", "Normal", ""),
    ("Beatriz Helena Costa", 31, "66666666666", "03/06/1993", "bia.costa@email.com", "Anual", "4666-6666-6666-6666"),
    ("Rafael Augusto Martins", 41, "77777777777", "27/04/1983", "rafael.martins@email.com", "Normal", ""),
    ("Juliana Cristina Barbosa", 26, "88888888888", "12/12/1998", "juliana.barbosa@email.com", "VIP", "4888-8888-8888-8888"),
    ("Pedro Henrique Ribeiro", 16, "99999999999", "30/08/2008", "pedro.ribeiro@email.com", "Normal", ""),
    ("Camila Fernanda Dias", 8, "10101010101", "14/02/2016", "camila.dias@email.com", "Normal", ""),

    # --- Gringos ---
    ("James Michael Carter", 38, "20202020202", "21/05/1986", "james.carter@email.com", "VIP", "5202-0202-0202-0202"),
    ("Emily Rose Thompson", 29, "30303030303", "07/10/1995", "emily.thompson@email.com", "Anual", "5303-0303-0303-0303"),
    ("William David Harris", 52, "40404040404", "19/01/1972", "william.harris@email.com", "Normal", ""),
    ("Sarah Elizabeth Walker", 24, "50505050505", "25/06/2000", "sarah.walker@email.com", "VIP", "5505-0505-0505-0505"),
    ("Daniel Thomas Wright", 33, "60606060606", "11/03/1991", "daniel.wright@email.com", "Normal", ""),
    ("Olivia Grace Bennett", 17, "70707070707", "09/09/2007", "olivia.bennett@email.com", "Anual", "5707-0707-0707-0707"),
    ("Michael Andrew Foster", 45, "80808080808", "02/12/1979", "michael.foster@email.com", "VIP", "5808-0808-0808-0808"),
    ("Sophie Marie Laurent", 11, "90909090909", "16/07/2013", "sophie.laurent@email.com", "Normal", ""),
    ("Christopher John Hayes", 55, "11011011011", "28/03/1969", "chris.hayes@email.com", "Anual", "6111-0110-1101-1011"),
    ("Emma Louise Parker", 27, "22022022022", "04/05/1997", "emma.parker@email.com", "Normal", ""),
]


def formatar_cpf(cpf):
    """Converte '11111111111' em '111.111.111-11' (mesmo padrão da GUI)."""
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def popular():
    """Garante as tabelas e insere os visitantes fictícios no banco real."""
    db.criar_tabelas()

    print(f"Inserindo {len(VISITANTES_SEED)} visitantes...")

    for nome, idade, cpf, data_nasc, email, tipo_passe, cartao in VISITANTES_SEED:
        cpf_formatado = formatar_cpf(cpf)
        v = Visitante(nome, idade, cpf_formatado, data_nasc, email, tipo_passe, cartao)
        db.salvar_visitante(v)
        print(f"  ✓ {nome} ({tipo_passe}) — CPF {cpf_formatado}")

    print("\nVisitantes no banco agora:")
    visitantes = db.carregar_visitantes()
    for v in visitantes:
        print(f"  - {v.nome} ({v.tipo_passe}) — CPF {v.cpf}")

    print(f"\nTotal: {len(visitantes)} visitantes.")


if __name__ == "__main__":
    popular()
    print("\nSeed concluído. Rode .venv/bin/python -m src.main para ver na GUI.")
