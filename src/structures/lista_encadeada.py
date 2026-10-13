
from src.structures.no import No


class ListaEncadeada:
    def __init__(self):
        # 'inicio' aponta para o primeiro nó da lista.
        # 'tamanho' guarda quantos elementos existem na lista.
        self.inicio = None
        self.tamanho = 0

    def inserir(self, dado):
        # Cria um novo nó que vai armazenar o dado informado.
        novo_no = No(dado)

        # Se a lista estiver vazia, o novo nó passa a ser o primeiro.
        if self.inicio is None:
            self.inicio = novo_no
        else:
            # Vai andando nó por nó até chegar ao último da lista.
            atual = self.inicio

            while atual.proximo is not None:
                atual = atual.proximo

            # Conecta o novo nó ao final da lista.
            atual.proximo = novo_no

        # Aumenta o número de elementos.
        self.tamanho += 1

    def buscar(self, dado):
        # Começa no início e percorre a lista até encontrar o valor.
        atual = self.inicio

        while atual is not None:
            # Se o dado do nó atual for igual ao procurado, retorna o valor.
            if atual.dado == dado:
                return atual.dado

            atual = atual.proximo

        # Se não encontrar, retorna None.
        return None

    def buscar_por(self, atributo, valor):
        # Percorre todos os nós para buscar um objeto cujo atributo tenha o valor informado.
        atual = self.inicio

        while atual is not None:
            dado = atual.dado

            # getattr(obj, atributo, None) tenta acessar o atributo do objeto.
            # Se ele existir e for igual ao valor, retorna o objeto completo.
            if getattr(dado, atributo, None) == valor:
                return dado

            atual = atual.proximo

        return None

    def remover(self, dado):
        # 'atual' é o nó sendo analisado e 'anterior' guarda o nó anterior.
        atual = self.inicio
        anterior = None

        while atual is not None:
            # Quando encontra o dado a ser removido:
            if atual.dado == dado:
                # Se o nó a remover for o primeiro da lista,
                # o início passa a apontar para o próximo nó.
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    # Se não for o primeiro, o nó anterior aponta para o próximo.
                    anterior.proximo = atual.proximo

                # Diminui o tamanho da lista.
                self.tamanho -= 1
                return atual.dado

            # Avança para o próximo nó, mantendo o anterior para ajuste do encadeamento.
            anterior = atual
            atual = atual.proximo

        # Se não encontrar o dado, retorna None.
        return None
