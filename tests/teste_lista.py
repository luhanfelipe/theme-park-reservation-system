
# Este arquivo contém testes manuais da ListaEncadeada.
# Ele facilita a verificação das operações de inserção,
# busca, remoção e busca por atributo durante o desenvolvimento.

from src.structures.lista_encadeada import ListaEncadeada
from src.models.visitante import Visitante


# Testes de inserção e tamanho
lista = ListaEncadeada()

lista.inserir("Visitante 1")
lista.inserir("Visitante 2")
lista.inserir("Visitante 3")

print("Tamanho:", lista.tamanho)

# Listagem dos elementos
atual = lista.inicio

while atual is not None:
    print(atual.dado)
    atual = atual.proximo


# Testes de busca
print("Busca:", lista.buscar("Visitante 2"))
print("Busca:", lista.buscar("Visitante 99"))


# Testes de remoção
print("Removido:", lista.remover("Visitante 2"))
print("Tamanho após remoção:", lista.tamanho)

atual = lista.inicio

while atual is not None:
    print(atual.dado)
    atual = atual.proximo

print("Removido:", lista.remover("Visitante 1"))
print("Tamanho após remover o primeiro:", lista.tamanho)

print("Removido:", lista.remover("Visitante 99"))
print("Tamanho após tentar remover inexistente:", lista.tamanho)


# Testes de busca por atributo em objetos
lista_visitantes = ListaEncadeada()

visitante = Visitante(
    "Ana Silva",
    20,
    "12345678901",
    "01/01/2006",
    "ana@email.com",
    "Normal"
)

lista_visitantes.inserir(visitante)

encontrado = lista_visitantes.buscar_por("cpf", "12345678901")
assert encontrado is visitante, "A busca deveria retornar o visitante cadastrado."

nao_encontrado = lista_visitantes.buscar_por("cpf", "00000000000")
assert nao_encontrado is None, "A busca deveria retornar None para um CPF inexistente."

print("Busca por atributo: testes concluídos!")
