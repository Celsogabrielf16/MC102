# Preenche um dicionário com a chave sendo o tipo da flecha e o valor a quantidade disponível da mesma
def preencheFlechasDisponiveis(lista: list) -> dict:
    dicionarioFinal: dict = {}
    for indice in range(0, len(lista), 2):
        dicionarioFinal[lista[indice]] = lista[indice + 1]
    return dicionarioFinal

# Preenche uma lista com as informações dos monstros dispostas em um dicionário
def preencheListaMonstros(quantidadeMonstros: int) -> list:
    listaFinal: list = []
    for _ in range(quantidadeMonstros):
        informacoesMonstro: list[int] = [int(info) for info in input().split(' ')]
        dictIformacoesMonstro: dict = {}
        dictIformacoesMonstro['pontosVida'] = informacoesMonstro[0]
        dictIformacoesMonstro['pontosAtaque'] = informacoesMonstro[1]
        dictIformacoesMonstro['quantidadePartes'] = informacoesMonstro[2]
        dictIformacoesMonstro['partes'] = {}
        for _ in range(informacoesMonstro[2]):
            partes: list = input().split(', ')
            dictIformacoesParte: list = [partes[1], int(partes[2]), (int(partes[3]), int(partes[4]))]
            dictIformacoesMonstro['partes'][partes[0]] = dictIformacoesParte
        listaFinal.append(dictIformacoesMonstro)
    return listaFinal

# Preenche um dicionário com as informações do ataque da Aloy
def preencheInformacoesAtaque(listaInfo: list) -> dict:
    dictFinal: dict = {}
    dictFinal['unidadeAlvo'] = int(listaInfo[0])
    dictFinal['parteAlvo'] = listaInfo[1]
    dictFinal['flechaUsada'] = listaInfo[2]
    dictFinal['cordenadasFlecha'] = (int(listaInfo[3]), int(listaInfo[4]))
    return dictFinal

def calculaDanoAtaque(infoMonstros, infoAtaque):
    cordenadaCritica: tuple = infoMonstros[infoAtaque['unidadeAlvo']]['partes'][infoAtaque['parteAlvo']][2]
    cordenadaFlecha: tuple = infoAtaque['cordenadasFlecha']
    danoMaximo: tuple = infoMonstros[infoAtaque['unidadeAlvo']]['partes'][infoAtaque['parteAlvo']][1]
    print(cordenadaCritica, cordenadaCritica[0], cordenadaCritica[1])
    """distanciaX: int = cordenadaCritica[0] - cordenadaFlecha[0]
     moduloCordenadaX: int = distanciaX if distanciaX > 0 else - distanciaX
    distanciaY: int = cordenadaCritica[0] - cordenadaFlecha[0]
    moduloCordenadaY: int = distanciaY if distanciaY > 0 else - distanciaY
    danoTotal: int = danoMaximo - (distanciaX + distanciaY) """
    print(cordenadaCritica, cordenadaFlecha)
    return

def main() -> None:
    pontosVidaAloy: int = int(input())
    flechasDisponiveis: dict[str, int] = preencheFlechasDisponiveis(input().split(' '))
    quantidadeMonstrosTotal: int = int(input())
    monstrosRestantes: int = quantidadeMonstrosTotal
    while monstrosRestantes != 0:
        quantidadeMonstrosCombate: int = int(input())
        listaMonstros: list[dict] = preencheListaMonstros(quantidadeMonstrosCombate)
        informacoesAtaque: dict = preencheInformacoesAtaque(input().split(', '))
        danoAtaque = calculaDanoAtaque(listaMonstros, informacoesAtaque)
        monstrosRestantes -= quantidadeMonstrosCombate

if __name__ == '__main__':
    main()