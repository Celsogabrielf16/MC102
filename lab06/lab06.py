def recebeVetor() -> list[int]:
    listaStr: list[str] = input().split(',')
    listaInt: list[int] = []
    for elemento in listaStr:
        listaInt.append(int(elemento))
    return listaInt


def verificaVetores(
            vetor1: list[int],
            vetor2: list[int],
            operacao: str,
            elemento: int
        ) -> list[list[int]]:
    if len(vetor1) == len(vetor2):
        return [vetor1, vetor2]
    elif len(vetor1) > len(vetor2):
        vetor2 = addNoVetor(vetor2, elemento, len(vetor1) - len(vetor2))
        return [vetor1, vetor2]
    elif len(vetor1) < len(vetor2):
        vetor1 = addNoVetor(vetor1, elemento, len(vetor2) - len(vetor1))
        return [vetor1, vetor2]
    else:
        return []


def addNoVetor(
            vetor: list[int],
            elemento: int,
            quantidadeElemento: int
        ) -> list[int]:
    for i in range(quantidadeElemento):
        vetor.append(elemento)
    return vetor


def operacaoBasica(
            vetor1: list[int],
            vetor2: list[int],
            operacao: str,
            elemento: int
        ) -> list[int]:
    vetoresPadronizados = verificaVetores(vetor1, vetor2, operacao, elemento)
    vetor1 = vetoresPadronizados[0]
    vetor2 = vetoresPadronizados[1]
    resultadoFinal: list[int] = []
    for i in range(len(vetor1)):
        match operacao:
            case 'soma':
                resultadoFinal.append(vetor1[i] + vetor2[i])
            case 'subtracao':
                resultadoFinal.append(vetor1[i] - vetor2[i])
            case 'multiplicacao':
                resultadoFinal.append(vetor1[i] * vetor2[i])
            case 'divisao':
                resultadoFinal.append(vetor1[i] // vetor2[i])
    return resultadoFinal


def soma_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    return operacaoBasica(vetor1, vetor2, 'soma', 0)


def subtrai_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    return operacaoBasica(vetor1, vetor2, 'subtracao', 0)


def multiplica_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    return operacaoBasica(vetor1, vetor2, 'multiplicacao', 1)


def divide_vetores(vetor1: list[int], vetor2: list[int]) -> list[int]:
    return operacaoBasica(vetor1, vetor2, 'divisao', 1)
    # Por algum motivo não funciona assim,
    # por isso tava com aquele if na função verificaVetores anteriormente


def multiplicacao_escalar(vetor: list[int], escalar: int) -> list[int]:
    resultadoFinal: list[int] = []
    for i in range(len(vetor)):
        resultadoFinal.append(vetor[i] * escalar)
    return resultadoFinal


def n_duplicacao(vetor: list[int], n: int) -> list[int]:
    if n == 0:
        return []
    else:
        resultadoFinal: list[int] = []
        for n in range(n):
            for elemento in vetor:
                resultadoFinal.append(elemento)
        return resultadoFinal


def soma_elementos(vetor: list[int]) -> int:
    soma: int = 0
    for elemento in vetor:
        soma += elemento
    return soma


def produto_interno(vetor1: list[int], vetor2: list[int]) -> int:
    vetorProduto = multiplica_vetores(vetor1, vetor2)
    return soma_elementos(vetorProduto)


def multiplica_todos(vetor1: list[int], vetor2: list[int]) -> list[int]:
    resultadoFinal: list[int] = []
    for elementoVetor1 in vetor1:
        soma = 0
        for elementoVetor2 in vetor2:
            soma += elementoVetor1 * elementoVetor2
        resultadoFinal.append(soma)
    return resultadoFinal


def correlacao_cruzada(vetor: list[int], mascara: list[int]) -> list[int]:
    resultadoFinal: list[int] = []
    for i in range(len(vetor) - len(mascara) + 1):
        vetorSeparado = vetor[slice(i, len(mascara) + i)]
        resultadoFinal.append(produto_interno(vetorSeparado, mascara))
    return resultadoFinal


if __name__ == "__main__":
    vetor1: list[int] = recebeVetor()
    executar: bool = True
    while executar:
        calculo: str = input()
        match calculo:
            case 'soma_vetores':
                vetor1 = soma_vetores(vetor1, recebeVetor())
            case 'subtrai_vetores':
                vetor1 = subtrai_vetores(vetor1, recebeVetor())
            case 'multiplica_vetores':
                vetor1 = multiplica_vetores(vetor1, recebeVetor())
            case 'divide_vetores':
                vetor1 = divide_vetores(vetor1, recebeVetor())
            case 'multiplicacao_escalar':
                vetor1 = multiplicacao_escalar(vetor1, int(input()))
            case 'n_duplicacao':
                vetor1 = n_duplicacao(vetor1, int(input()))
            case 'soma_elementos':
                vetor1 = [soma_elementos(vetor1)]
            case 'produto_interno':
                vetor1 = [produto_interno(vetor1, recebeVetor())]
            case 'multiplica_todos':
                vetor1 = multiplica_todos(vetor1, recebeVetor())
            case 'correlacao_cruzada':
                vetor1 = correlacao_cruzada(vetor1, recebeVetor())
            case 'fim':
                executar = False
        if executar:
            print(vetor1)
