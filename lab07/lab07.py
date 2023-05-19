def encontraChave(operador: str, primeiroOperando: str, segundoOperando: str) -> int:
    indicePrimeiroOperando: int = defineIndiceOperando(primeiroOperando)
    indiceSegundoOperando: int = defineIndiceOperando(segundoOperando, indicePrimeiroOperando)
    match operador:
        case '+':
            return indicePrimeiroOperando + indiceSegundoOperando
        case '-':
            return indicePrimeiroOperando - indiceSegundoOperando
        case '*':
            return indicePrimeiroOperando * indiceSegundoOperando


def defineIndiceOperando(operando: str, indicePrimeiroOperando: int = 0) -> int:
    match operando:
        case 'vogal':
            vogais: str = 'aeiouAEIOU'
            return encontraIndiceCaractere(vogais)
        case 'consoante':
            consoantes: str = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
            return encontraIndiceCaractere(consoantes)
        case 'numero':
            numeros: str = '0123456789'
            return encontraIndiceCaractere(numeros)
        case _:
            return linhasJuntas.index(operando, indicePrimeiroOperando)


def encontraIndiceCaractere(caracteresDesejados: str) -> int:
    for caractere in linhasJuntas:
        if caractere in caracteresDesejados:
            return linhasJuntas.index(caractere)


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


operador: str = input()
primeiroOperando: str = input()
segundoOperando: str = input()
numeroLinhas: int = int(input())
linhas: list[str] = []

for i in range(numeroLinhas):
    linhas.append(input())
linhasJuntas: str = ''.join(linhas)

chave: int = encontraChave(operador, primeiroOperando, segundoOperando)
linhasDescriptografada: list[str] = descriptografar(linhas, chave)

print(chave)
for linha in linhasDescriptografada:
    print(linha)
