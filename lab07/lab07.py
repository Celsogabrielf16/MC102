# Encontra a chave decodificadora
def encontraChave(operador: str, primeiroOperando: str, segundoOperando: str, linhasJuntas: str) -> int:
    indicePrimeiroOperando: int = defineIndiceOperando(primeiroOperando, linhasJuntas)
    indiceSegundoOperando: int = defineIndiceOperando(segundoOperando, linhasJuntas, indicePrimeiroOperando)
    match operador:
        case '+':
            return indicePrimeiroOperando + indiceSegundoOperando
        case '-':
            return indicePrimeiroOperando - indiceSegundoOperando
        case '*':
            return indicePrimeiroOperando * indiceSegundoOperando


# Faz uma verificação e direciona para a função que encontra o indice do caractere de acordo com seu tipo
def defineIndiceOperando(operando: str, linhasJuntas: str, indicePrimeiroOperando: int = 0) -> int:
    match operando:
        case 'vogal':
            vogais: str = 'aeiouAEIOU'
            return encontraIndiceCaractere(vogais, linhasJuntas)
        case 'consoante':
            consoantes: str = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
            return encontraIndiceCaractere(consoantes, linhasJuntas)
        case 'numero':
            numeros: str = '0123456789'
            return encontraIndiceCaractere(numeros, linhasJuntas)
        case _:
            return linhasJuntas.index(operando, indicePrimeiroOperando)


# Define o indice onde se encontra o caractere desejado 
def encontraIndiceCaractere(caracteresDesejados: str, linhasJuntas: str) -> int:
    for caractere in linhasJuntas:
        if caractere in caracteresDesejados:
            return linhasJuntas.index(caractere)


# Usa a chave encontrada para decodificar a mensagem desejada
def descriptografar(linhas: list[str], chave: int) -> list[str]:
    if chave > 95:
        chave = chave % 95
    resultadoFinal: list[str] = []
    for linha in linhas:
        novaLinha: list[str] = []
        for caractere in linha:
            representacaoDecimal = ord(caractere) + chave
            if representacaoDecimal > 126:
                caractereDescriptografado = chr(representacaoDecimal - 95)
            elif representacaoDecimal < 32:
                caractereDescriptografado = chr(representacaoDecimal + 95)
            else:
                caractereDescriptografado = chr(representacaoDecimal)
            novaLinha.append(caractereDescriptografado)
        resultadoFinal.append(''.join(novaLinha))
    return resultadoFinal


def main() -> None:
    operador: str = input()
    primeiroOperando: str = input()
    segundoOperando: str = input()
    numeroLinhas: int = int(input())
    linhas: list[str] = []

    for _ in range(numeroLinhas):
        linhas.append(input())
    linhasJuntas: str = ''.join(linhas)

    chave: int = encontraChave(operador, primeiroOperando, segundoOperando, linhasJuntas)
    linhasDescriptografada: list[str] = descriptografar(linhas, chave)

    print(chave)
    for linha in linhasDescriptografada:
        print(linha)


if __name__ == '__main__':
    main()
