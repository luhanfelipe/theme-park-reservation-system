# Este arquivo contém testes manuais da ListaEncadeada.
# Ele é mantido no projeto para facilitar a verificação das operações
# de inserção, busca e remoção durante o desenvolvimento.

from src.structures.lista_encadeada import ListaEncadeada

lista = ListaEncadeada()

lista.inserir("Visitante 1")
lista.inserir("Visitante 2")
lista.inserir("Visitante 3")

print("Tamanho:", lista.tamanho)

atual = lista.inicio

while atual is not None:
    print(atual.dado)
    atual = atual.proximo

# Primeiros testes de busca
print("Busca:", lista.buscar("Visitante 2"))
print("Busca:", lista.buscar("Visitante 99"))

# Testes de Remoção
print("Removido:", lista.remover("Visitante 2"))
print("Tamanho após remoção:", lista.tamanho)

atual = lista.inicio

while atual is not None:
    print(atual.dado)
    atual = atual.proximo

# Outros testes sugeridos por IA para desenvolvimento inicial
print("Removido:", lista.remover("Visitante 1"))
print("Tamanho após remover o primeiro:", lista.tamanho)

print("Removido:", lista.remover("Visitante 99"))
print("Tamanho após tentar remover inexistente:", lista.tamanho)
