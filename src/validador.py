def luhn_check(card_number: str) -> bool:
    """
    Valida o número do cartão usando o algoritmo de Luhn.

    O algoritmo de Luhn é utilizado para verificar se um número de cartão de crédito é potencialmente válido.
    Ele faz isso somando os dígitos do cartão de uma forma específica e verificando se o resultado é divisível por 10.
    """
    # Remove espaços e traços do número do cartão
    card_number = card_number.replace(" ", "").replace("-", "")
    # Verifica se o número contém apenas dígitos
    if not card_number.isdigit():
        return False
    total = 0  # Acumulador para a soma dos dígitos processados
    reverse_digits = card_number[::-1]  # Inverte o número para processar da direita para a esquerda
    for i, digit in enumerate(reverse_digits):
        n = int(digit)  # Converte o caractere para inteiro
        if i % 2 == 1:  # Para cada segundo dígito (começando do índice 1)
            n *= 2      # Multiplica o dígito por 2
            if n > 9:   # Se o resultado for maior que 9, subtrai 9 (equivalente a somar os dígitos)
                n -= 9
        total += n      # Soma ao total
    # Retorna True se o total for divisível por 10, caso contrário False
    return total % 10 == 0

def in_interval(prefix: str, interval: str) -> bool:
    """
    Verifica se o prefixo está dentro do intervalo especificado (ex: '51-55').

    Parâmetros:
    - prefix: prefixo a ser verificado (string numérica)
    - interval: intervalo no formato 'inicio-fim' (ex: '51-55')

    Retorna:
    - True se o prefixo está dentro do intervalo, False caso contrário.
    """
    start, end = interval.split('-')  # Divide o intervalo em início e fim
    # Converte para inteiro e verifica se o prefixo está dentro do intervalo
    return int(start) <= int(prefix) <= int(end)

def get_bandeira(card_number: str) -> str:
    """
    Retorna a bandeira do cartão de acordo com os prefixos conhecidos.

    O método percorre uma lista de tuplas contendo o nome da bandeira e seus prefixos.
    Para cada prefixo, verifica se o número do cartão começa com esse valor ou está dentro do intervalo.
    Retorna o nome da bandeira correspondente ou None se não encontrar.
    """
    # Remove espaços e traços do número do cartão
    card_number = card_number.replace(" ", "").replace("-", "")
    # Verifica se o número contém apenas dígitos
    if not card_number.isdigit():
        return None

    # Lista de tuplas: (nome da bandeira, lista de prefixos)
    # Cada prefixo é uma tupla (tamanho do prefixo, valor ou intervalo)
    bandeiras = [
        ("MasterCard", [("2", "2221-2720"), ("2", "51-55")]),
        ("Visa", [("1", "4")]),
        ("American Express", [("2", "34"), ("2", "37")]),
        ("Diners Club", [("3", "300-305"), ("4", "3095"), ("2", "36"), ("2", "38"), ("2", "39")]),
        ("Discover", [("4", "6011"), ("6", "622126-622925"), ("3", "644-649"), ("2", "65")]),
        ("enRoute", [("4", "2014"), ("4", "2149")]),
        ("JCB", [("4", "3528-3589")]),
        ("Voyager", [("4", "8699"), ("4", "7088")]),
        ("Hipercard", [
            ("6", "384100-384110"), ("6", "384140-384160"), ("6", "606282-606290"),
            ("6", "637095-637103"), ("6", "637568-637570"), ("6", "637573-637576"),
            ("6", "637578-637580")
        ]),
        ("Aura", [("2", "50")]),
        ("Elo", [
            ("4", "4011"), ("4", "4312"), ("4", "4389"), ("4", "4514"), ("4", "4573"), ("4", "4576"),
            ("4", "5041"), ("4", "5066"), ("4", "5067"), ("4", "5090"), ("4", "6277"), ("4", "6362"),
            ("4", "6363"), ("4", "6500-6505"), ("6", "650485-650531"), ("6", "650532-650538"),
            ("6", "650541-650598"), ("6", "650700-650718"), ("6", "650720-650727")
        ]),
        ("Visa Electron", [("4", "4026"), ("6", "417500"), ("4", "4508"), ("4", "4844"), ("4", "4913"), ("4", "4917")]),
        ("Maestro", [("2", "50"), ("2", "56-69")]),
        ("Solo", [("4", "6334"), ("4", "6767")]),
        ("Switch", [("4", "4903"), ("4", "4905"), ("4", "4911"), ("4", "4936"), ("6", "564182"), ("6", "633110"), ("4", "6333"), ("4", "6759")]),
        ("Laser", [("4", "6304"), ("4", "6706"), ("4", "6771"), ("4", "6709")]),
        ("UnionPay", [("2", "62")]),
        ("Cabal", [("4", "6042"), ("4", "6043")])
    ]

    # Para cada bandeira e seus prefixos
    for bandeira, prefixos in bandeiras:
        for tamanho, valor in prefixos:
            if '-' in valor:
                # Se o valor é um intervalo, divide em início e fim
                inicio, fim = valor.split('-')
                prefixo = card_number[:len(inicio)]  # Pega o prefixo do cartão com o mesmo tamanho do início
                # Verifica se o prefixo está dentro do intervalo
                if len(prefixo) == len(inicio) and inicio <= prefixo <= fim:
                    return bandeira
            else:
                # Se não for intervalo, compara diretamente
                prefixo = card_number[:len(valor)]
                if prefixo == valor:
                    return bandeira
    # Se não encontrar nenhuma bandeira, retorna None
    return None

def validar_cartao(card_number: str) -> dict:
    """
    Valida o cartão e retorna informações sobre validade e bandeira.

    Parâmetros:
    - card_number: número do cartão (string)

    Retorna:
    - dict com as chaves 'valido' (bool) e 'bandeira' (str ou None)
    """
    valido = luhn_check(card_number)      # Verifica se o cartão é válido pelo algoritmo de Luhn
    bandeira = get_bandeira(card_number)  # Identifica a bandeira do cartão
    return {
        "valido": valido,
        "bandeira": bandeira
    }

# Exemplo de uso:
if __name__ == "__main__":
    numero = input("Digite o número do cartão: ")
    resultado = validar_cartao(numero)
    if resultado["bandeira"]:
        print(f"Bandeira: {resultado['bandeira']}")
    else:
        print("Bandeira não identificada.")
    print("Cartão válido pelo Luhn?" , "Sim" if resultado["valido"] else "Não")