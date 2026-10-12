def formatar_cpf(texto):
    """Recebe '11111111111' (ou com pontos/traços) e devolve '111.111.111-11'.
    Se não tiver 11 dígitos, devolve o texto original sem formatação."""
    apenas_numeros = "".join(filter(str.isdigit, texto))
    if len(apenas_numeros) != 11:
        return texto
    return f"{apenas_numeros[:3]}.{apenas_numeros[3:6]}.{apenas_numeros[6:9]}-{apenas_numeros[9:]}"
