from src.structures.lista_encadeada import ListaEncadeada
from src.models.visitante import Visitante
from src.models.atracao import Atracao
from src.models.reserva import Reserva
from src.database import db


ADMIN_USUARIO = "admin"
ADMIN_SENHA = "admin123"


class ParqueService:
    def __init__(self):
        """Inicializa as listas encadeadas e carrega os dados persistidos."""
        self.visitantes = ListaEncadeada()
        self.atracoes = ListaEncadeada()
        self.reservas = ListaEncadeada()

        db.criar_tabelas()

        for v in db.carregar_visitantes():
            self.visitantes.inserir(v)

        for a in db.carregar_atracoes():
            self.atracoes.inserir(a)

        for r in db.carregar_reservas():
            self.reservas.inserir(r)

    def cadastrar_visitante(self, nome, idade, cpf, data_nascimento, email, tipo_passe, cartao="", senha=""):
        """Cria um visitante, armazena-o em memória e persiste no banco."""
        novo_visitante = Visitante(nome, idade, cpf, data_nascimento, email, tipo_passe, cartao, senha)
        self.visitantes.inserir(novo_visitante)
        db.salvar_visitante(novo_visitante)
        return "Visitante cadastrado com sucesso!"

    def cadastrar_atracao(self, nome, tipo, capacidade, idade_minima, horario, aceita_prioridade):
        """Cria uma atração, armazena-a em memória e persiste no banco."""
        nova_atracao = Atracao(nome, tipo, capacidade, idade_minima, horario, aceita_prioridade)
        self.atracoes.inserir(nova_atracao)
        db.salvar_atracao(nova_atracao)
        return "Atração cadastrada com sucesso!"

    def autenticar_visitante(self, cpf, senha):
        """Retorna o Visitante se CPF e senha baterem, senão None."""
        visitante = self.visitantes.buscar_por("cpf", cpf)
        if visitante is None:
            return None
        if visitante.senha != senha:
            return None
        return visitante

    def autenticar_admin(self, usuario, senha):
        """Retorna True se usuário e senha baterem com o admin hardcoded."""
        return usuario == ADMIN_USUARIO and senha == ADMIN_SENHA

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

    # --- MÉTODOS DA ISSUE #10 (RESERVAS) ---

    def criar_reserva(self, cpf, nome_atracao, horario):
        """Valida regras de negócio e cria uma nova reserva."""
        visitante = self.visitantes.buscar_por("cpf", cpf)
        if visitante is None:
            return False, "Visitante não encontrado."

        atracao = self.atracoes.buscar_por("nome", nome_atracao)
        if atracao is None:
            return False, "Atração não encontrada."

        reservas_ativas = []
        atual = self.reservas.inicio
        while atual is not None:
            r = atual.dado
            if r.cpf_visitante == cpf and r.status == "Ativa":
                reservas_ativas.append(r)
            atual = atual.proximo

        for r in reservas_ativas:
            if r.horario == horario:
                return False, "Você já possui uma reserva ativa para este mesmo horário."

        tipo_passe = str(getattr(visitante, 'tipo_passe', 'Normal')).upper()
        if "VIP" in tipo_passe:
            limite = 3
        elif "ANUAL" in tipo_passe:
            limite = 2
        else:
            limite = 1

        if len(reservas_ativas) >= limite:
            return False, f"Limite de reservas ativas atingido ({limite} para o passe {getattr(visitante, 'tipo_passe', 'Normal')})."

        nova_reserva = Reserva(cpf_visitante=cpf, nome_atracao=atracao.nome, horario=horario)
        self.reservas.inserir(nova_reserva)
        db.salvar_reserva(nova_reserva)

        if hasattr(atracao, 'fila_virtual'):
            atracao.fila_virtual.enfileirar(visitante, atracao.aceita_prioridade)

        return True, nova_reserva

    def listar_reservas_do_visitante(self, cpf):
        """Retorna a lista de reservas atreladas ao CPF informado."""
        lista = []
        atual = self.reservas.inicio
        while atual is not None:
            if atual.dado.cpf_visitante == cpf:
                lista.append(atual.dado)
            atual = atual.proximo
        return lista

    def cancelar_reserva(self, codigo, e_visitante=True):
        """Cancela uma reserva existente e atualiza o banco de dados."""
        if not e_visitante:
            return False, "Apenas o visitante pode cancelar suas próprias reservas."

        reserva_encontrada = self.reservas.buscar_por("codigo", codigo)
        if reserva_encontrada is None:
            return False, "Reserva não encontrada."

        if reserva_encontrada.status == "Cancelada":
            return False, "Esta reserva já está cancelada."

        reserva_encontrada.cancelar()
        db.atualizar_status_reserva(codigo, "Cancelada")

        return True, "Reserva cancelada com sucesso."

    def listar_reservas(self):
        """Retorna todas as reservas registradas no sistema (para uso do painel admin)."""
        lista = []
        atual = self.reservas.inicio
        while atual is not None:
            lista.append(atual.dado)
            atual = atual.proximo
        return lista
