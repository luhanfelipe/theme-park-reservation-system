import os
import sqlite3

from src.models.visitante import Visitante
from src.models.atracao import Atracao
from src.models.reserva import Reserva


CAMINHO_BANCO = os.path.join("data", "parque.db")

def conectar():
    """Abre conexão com o banco. Cria a pasta data/ se ela não existir."""
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabelas():
    """Cria as tabelas visitantes, atracoes e reservas se ainda não existirem."""
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS visitantes (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                data_nascimento TEXT NOT NULL,
                email TEXT NOT NULL,
                tipo_passe TEXT NOT NULL,
                cartao TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS atracoes (
                nome TEXT PRIMARY KEY,
                tipo TEXT NOT NULL,
                capacidade INTEGER NOT NULL,
                idade_minima INTEGER NOT NULL,
                horario TEXT NOT NULL,
                aceita_prioridade INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                codigo TEXT PRIMARY KEY,
                cpf_visitante TEXT NOT NULL,
                nome_atracao TEXT NOT NULL,
                horario TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()


def salvar_visitante(visitante):
    """Insere um visitante no banco. Ignora se o CPF já existir."""
    with conectar() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO visitantes
                (cpf, nome, idade, data_nascimento, email, tipo_passe, cartao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            visitante.cpf,
            visitante.nome,
            int(visitante.idade),
            visitante.data_nascimento,
            visitante.email,
            visitante.tipo_passe,
            getattr(visitante, "cartao", "") or ""
        ))
        conn.commit()


def salvar_atracao(atracao):
    """Insere uma atração no banco. Ignora se o nome já existir."""
    with conectar() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO atracoes
                (nome, tipo, capacidade, idade_minima, horario, aceita_prioridade)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            atracao.nome,
            atracao.tipo,
            int(atracao.capacidade),
            int(atracao.idade_minima),
            atracao.horario,
            1 if atracao.aceita_prioridade else 0
        ))
        conn.commit()


def salvar_reserva(reserva):
    """Insere uma reserva no banco."""
    with conectar() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO reservas
                (codigo, cpf_visitante, nome_atracao, horario, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            reserva.codigo,
            reserva.cpf_visitante,
            reserva.nome_atracao,
            reserva.horario,
            reserva.status
        ))
        conn.commit()


def atualizar_status_reserva(codigo, novo_status):
    """Atualiza o status de uma reserva específica pelo código."""
    with conectar() as conn:
        conn.execute("""
            UPDATE reservas
            SET status = ?
            WHERE codigo = ?
        """, (novo_status, codigo))
        conn.commit()


def carregar_visitantes():
    """Retorna uma lista de objetos Visitante vindos do banco."""
    with conectar() as conn:
        cursor = conn.execute("""
            SELECT nome, idade, cpf, data_nascimento, email, tipo_passe, cartao
            FROM visitantes
        """)
        return [
            Visitante(nome, idade, cpf, data_nascimento, email, tipo_passe, cartao or "")
            for (nome, idade, cpf, data_nascimento, email, tipo_passe, cartao) in cursor.fetchall()
        ]


def carregar_atracoes():
    """Retorna uma lista de objetos Atracao vindos do banco."""
    with conectar() as conn:
        cursor = conn.execute("""
            SELECT nome, tipo, capacidade, idade_minima, horario, aceita_prioridade
            FROM atracoes
        """)
        return [
            Atracao(nome, tipo, capacidade, idade_minima, horario, bool(aceita_prioridade))
            for (nome, tipo, capacidade, idade_minima, horario, aceita_prioridade) in cursor.fetchall()
        ]


def carregar_reservas():
    """Retorna uma lista de objetos Reserva vindos do banco."""
    with conectar() as conn:
        cursor = conn.execute("""
            SELECT codigo, cpf_visitante, nome_atracao, horario, status
            FROM reservas
        """)
        return [
            Reserva(
                cpf_visitante=cpf_visitante,
                nome_atracao=nome_atracao,
                horario=horario,
                status=status,
                codigo=codigo
            )
            for (codigo, cpf_visitante, nome_atracao, horario, status) in cursor.fetchall()
        ]