from src.structures.no import No


class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0

    def inserir(self, dado):
        novo_no = No(dado)

        if self.inicio is None:
            self.inicio = novo_no
        else:
            atual = self.inicio

            while atual.proximo is not None:
                atual = atual.proximo

            atual.proximo = novo_no

        self.tamanho += 1

    def buscar(self, dado):
        atual = self.inicio

        while atual is not None:
            if atual.dado == dado:
                return atual.dado

            atual = atual.proximo

        return None

    def remover(self, dado):
        atual = self.inicio
        anterior = None

        while atual is not None:
            if atual.dado == dado:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo

                self.tamanho -= 1
                return atual.dado

            anterior = atual
            atual = atual.proximo

        return None
