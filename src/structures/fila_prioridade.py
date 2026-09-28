from src.structures.no import No

class FilaPrioridade:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0

    def enfileirar(self, visitante, atracao_aceita_prioridade):
        novo_no = No(visitante)

        # Se a fila está vazia, apenas entra
        if self.inicio is None:
            self.inicio = novo_no
        else:
            # Se a atração aceita prioridade E o novo visitante é VIP/Especial E o primeiro da fila é Normal
            if atracao_aceita_prioridade and visitante.tipo_passe != "Normal" and self.inicio.dado.tipo_passe == "Normal":
                # VIP fura a fila e vira o primeiro
                novo_no.proximo = self.inicio
                self.inicio = novo_no
            else:
                # Caso contrário, percorre a fila para achar o lugar certo
                atual = self.inicio
                
                # Continua andando na fila enquanto:
                # 1. Existir um próximo
                # 2. NÃO acontecer a situação do VIP achar um "Normal" na frente dele (se a atração aceitar prioridade)
                while atual.proximo is not None:
                    proximo_visitante = atual.proximo.dado
                    if atracao_aceita_prioridade and visitante.tipo_passe != "Normal" and proximo_visitante.tipo_passe == "Normal":
                        break # Achou o ponto onde o VIP deve furar a fila
                    atual = atual.proximo
                
                # Insere na posição encontrada
                novo_no.proximo = atual.proximo
                atual.proximo = novo_no

        self.tamanho += 1

    def desenfileirar(self):
        # Remove a pessoa do início da fila para entrar no brinquedo
        if self.inicio is None:
            return None
        
        atendido = self.inicio.dado
        self.inicio = self.inicio.proximo
        self.tamanho -= 1
        return atendido

    def listar_fila(self):
        # Apenas para facilitar a visualização da fila
        elementos = []
        atual = self.inicio
        while atual is not None:
            elementos.append(f"{atual.dado.nome} ({atual.dado.tipo_passe})")
            atual = atual.proximo
        return elementos