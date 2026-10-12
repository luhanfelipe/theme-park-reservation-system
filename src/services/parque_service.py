from src.structures.lista_encadeada import ListaEncadeada
from src.models.visitante import Visitante
from src.models.atracao import Atracao
from src.database import db


class ParqueService:
    def __init__(self):
        """Inicializa as listas encadeadas e carrega os dados persistidos."""
        self.visitantes = ListaEncadeada()
        self.atracoes = ListaEncadeada()

        db.criar_tabelas()

        for v in db.carregar_visitantes():
            self.visitantes.inserir(v)

        for a in db.carregar_atracoes():
            self.atracoes.inserir(a)

    def cadastrar_visitante(self, nome, idade, cpf, data_nascimento, email, tipo_passe, cartao=""):
        """Cria um visitante, armazena-o em memória e persiste no banco."""
        novo_visitante = Visitante(nome, idade, cpf, data_nascimento, email, tipo_passe, cartao)
        self.visitantes.inserir(novo_visitante)
        db.salvar_visitante(novo_visitante)
        return "Visitante cadastrado com sucesso!"

    def cadastrar_atracao(self, nome, tipo, capacidade, idade_minima, horario, aceita_prioridade):
        """Cria uma atração, armazena-a em memória e persiste no banco."""
        nova_atracao = Atracao(nome, tipo, capacidade, idade_minima, horario, aceita_prioridade)
        self.atracoes.inserir(nova_atracao)
        db.salvar_atracao(nova_atracao)
        return "Atração cadastrada com sucesso!"

    def listar_visitantes(self):
        """Converte os visitantes da lista encadeada em uma lista comum para a GUI."""
        lista = []
        atual = self.visitantes.inicio
        while atual is not None:
            lista.append(atual.dado)
            atual = atual.proximo
        return lista

    def listar_atracoes(self):
        """Converte as atrações da lista encadeada em uma lista comum para a GUI."""
        lista = []
        atual = self.atracoes.inicio
        while atual is not None:
            lista.append(atual.dado)
            atual = atual.proximo
        return lista

    def adicionar_visitante_na_fila(self, cpf, nome_atracao):
        """Valida visitante e atração e adiciona o visitante à fila."""

        visitante_encontrado = self.visitantes.buscar_por("cpf", cpf)

        if visitante_encontrado is None:
            return "Erro: Visitante não encontrado."

        atracao_encontrada = self.atracoes.buscar_por("nome", nome_atracao)

        if atracao_encontrada is None:
            return "Erro: Atração não encontrada."

        if int(visitante_encontrado.idade) < atracao_encontrada.idade_minima:
            return (
                f"Erro: {visitante_encontrado.nome} não tem a idade mínima "
                f"para {atracao_encontrada.nome}."
            )

        atracao_encontrada.fila_virtual.enfileirar(
            visitante_encontrado,
            atracao_encontrada.aceita_prioridade
        )

        return (
            f"Sucesso: {visitante_encontrado.nome} entrou na fila "
            f"para {atracao_encontrada.nome}!"
        )
