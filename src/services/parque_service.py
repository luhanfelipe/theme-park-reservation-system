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
        # 1. Encontrar o visitante
        visitante = self.buscar_visitante_por_cpf(cpf)
        if not visitante:
            return "Erro: Visitante não encontrado."

        # 2. Definir o limite de reservas com base no passe
        tipo_passe = str(visitante.tipo_passe).upper()
        if "VIP" in tipo_passe:
            limite = 3
        elif "ANUAL" in tipo_passe:
            limite = 2
        else:
            limite = 1

        # 3. Filtrar as reservas ativas deste visitante (Blindado para List ou ListaEncadeada)
        ativas = []
        if isinstance(self.reservas, list):
            ativas = [r for r in self.reservas if getattr(r, 'cpf_visitante', '') == cpf and getattr(r, 'status', '') == "Ativa"]
        else:
            atual = self.reservas.inicio
            while atual is not None:
                r = atual.dado
                if getattr(r, 'cpf_visitante', '') == cpf and getattr(r, 'status', '') == "Ativa":
                    ativas.append(r)
                atual = atual.proximo

        # 4. Validar Regra 1: Limite máximo
        if len(ativas) >= limite:
            return f"Erro: Limite de reservas ativas atingido ({limite} para passe {visitante.tipo_passe})."

        # 5. Validar Regra 2: Conflito de horário
        for r in ativas:
            if getattr(r, 'horario', '') == horario:
                return "Erro: Já possui uma reserva ativa para este horário."

        # 6. Criar, Adicionar na memória e Persistir
        nova_reserva = Reserva(cpf, nome_atracao, horario)
        
        if isinstance(self.reservas, list):
            self.reservas.append(nova_reserva)
        else:
            if hasattr(self.reservas, 'adicionar'):
                self.reservas.adicionar(nova_reserva)
            else:
                self.reservas.append(nova_reserva)

        # Envia o objeto inteiro para o banco (1 único argumento)
        db.salvar_reserva(nova_reserva)
        
        return nova_reserva
    def listar_reservas_do_visitante(self, cpf):
        """Retorna as reservas de um visitante específico (aceita Lista ou ListaEncadeada)."""
        reservas_encontradas = []
        
        # Se for uma lista normal do Python (ex: veio do banco de dados)
        if isinstance(self.reservas, list):
            for r in self.reservas:
                if getattr(r, 'cpf_visitante', '') == cpf:
                    reservas_encontradas.append(r)
        
        # Se for a estrutura customizada ListaEncadeada
        else:
            atual = self.reservas.inicio
            while atual is not None:
                reserva = atual.dado
                if getattr(reserva, 'cpf_visitante', '') == cpf:
                    reservas_encontradas.append(reserva)
                atual = atual.proximo
                
        return reservas_encontradas

    def cancelar_reserva(self, codigo):
        """Cancela uma reserva no banco e na memória (aceita Lista ou ListaEncadeada)."""
        # 1. Atualiza no banco de dados primeiro
        from src.database import db
        db.atualizar_status_reserva(codigo, "Cancelada")
        
        # 2. Atualiza na memória
        if isinstance(self.reservas, list):
            for reserva in self.reservas:
                if getattr(reserva, 'codigo', '') == codigo:
                    reserva.status = "Cancelada"
                    return "Reserva cancelada com sucesso."
        else:
            no_atual = self.reservas.inicio
            while no_atual is not None:
                reserva = no_atual.dado
                if getattr(reserva, 'codigo', '') == codigo:
                    reserva.status = "Cancelada"
                    return "Reserva cancelada com sucesso."
                no_atual = no_atual.proximo
                
        return "Erro: Reserva não encontrada."

    def listar_reservas(self):
        # Força o sistema a ir buscar os dados atualizados ao banco sempre que a tela Admin abre
        from src.database import db
        self.reservas = db.carregar_reservas()
        return self.reservas

    def buscar_visitante_por_cpf(self, cpf):
        """Busca um visitante cadastrado pelo seu CPF."""
        # Usa a função de listar que já existe no seu serviço
        visitantes = self.listar_visitantes() 
        
        for visitante in visitantes:
            if visitante.cpf == cpf:
                return visitante
                
        return None
