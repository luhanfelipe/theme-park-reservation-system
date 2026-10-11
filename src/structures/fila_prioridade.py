class No:
    def __init__(self, visitante):
        self.visitante = visitante
        self.proximo = None

class FilaPrioridade:
    def __init__(self):
        self.inicio = None

    def _obter_peso(self, visitante):
        # Transforma o passe em maiúsculo para evitar erros de digitação (ex: "Vip", "vip", "VIP")
        passe = str(visitante.tipo_passe).upper() 
        
        if "VIP" in passe:
            return 3
        elif "ANUAL" in passe:
            return 2
        else:
            return 1  # Se não for VIP nem Anual, é Normal

    def enfileirar(self, visitante, atracao_aceita_prioridade=True):
        novo_no = No(visitante)

        # Se a atração NÃO aceita prioridade, todo mundo é tratado como Peso 1 (Normal)
        peso_novo = self._obter_peso(visitante) if atracao_aceita_prioridade else 1

        # CASO 1: A fila está vazia ou o novo visitante tem MAIS prioridade que o 1º da fila
        if self.inicio is None or peso_novo > self._obter_peso(self.inicio.visitante):
            novo_no.proximo = self.inicio
            self.inicio = novo_no
            return

        # CASO 2: Procurar a posição correta no meio ou fim da fila
        # O novo visitante vai andando para trás até achar alguém com prioridade MENOR que a dele
        atual = self.inicio
        while atual.proximo is not None:
            peso_proximo = self._obter_peso(atual.proximo.visitante) if atracao_aceita_prioridade else 1
            
            # Se o próximo da fila tem prioridade maior ou IGUAL, nós continuamos andando para trás
            if peso_proximo >= peso_novo:
                atual = atual.proximo
            else:
                break # Achamos o ponto de inserção!

        # Insere o novo nó conectando os ponteiros
        novo_no.proximo = atual.proximo
        atual.proximo = novo_no

    def listar_fila(self):
        # Retorna uma lista normal do Python apenas para a tela conseguir ler e desenhar
        elementos = []
        atual = self.inicio
        while atual is not None:
            elementos.append(atual.visitante)
            atual = atual.proximo
        return elementos