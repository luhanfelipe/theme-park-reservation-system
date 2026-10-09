from src.structures.lista_encadeada import ListaEncadeada
from src.models.visitante import Visitante
from src.models.atracao import Atracao

class ParqueService:
    def __init__(self):
        """Inicializa as listas encadeadas de visitantes e atrações do parque."""
        self.visitantes = ListaEncadeada()
        self.atracoes = ListaEncadeada()

    def cadastrar_visitante(self, nome, idade, cpf, data_nascimento, email, tipo_passe):
        """Cria um visitante, armazena-o e informa se o cadastro foi concluído."""
        novo_visitante = Visitante(nome, idade, cpf, data_nascimento, email, tipo_passe)
        self.visitantes.inserir(novo_visitante)
        return "Visitante cadastrado com sucesso!"

    def cadastrar_atracao(self, nome, capacidade, idade_minima, horario, aceita_prioridade):
        """Cria uma atração, armazena-a e informa se o cadastro foi concluído."""
        nova_atracao = Atracao(nome, capacidade, idade_minima, horario, aceita_prioridade)
        self.atracoes.inserir(nova_atracao)
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
