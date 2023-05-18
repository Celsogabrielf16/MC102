def preencheDicionario(lista: list) -> dict:
    dicionarioFinal: dict = {}
    for indice in range(0, len(lista), 2):
        dicionarioFinal[lista[indice]] = lista[indice + 1]
    return dicionarioFinal

def preencheListaMonstros(quantidadeMonstros: int) -> list:
    listaFinal: list = []
    for _ in range(quantidadeMonstros):
        informacoesMonstro: list[int] = [int(info) for info in input().split(' ')]
        print(informacoesMonstro)
    return list()

def main() -> None:
    pontosVidaAloy: int = int(input())
    flechasDisponiveis: dict[str, int] = preencheDicionario(input().split(' '))
    quantidadeMonstrosTotal: int = int(input())
    monstrosRestantes: int = quantidadeMonstrosTotal
    while monstrosRestantes != 0:
        quantidadeMonstrosCombate: int = int(input())
        listaMonstros: list[dict] = preencheListaMonstros(quantidadeMonstrosCombate)
        monstrosRestantes -= quantidadeMonstrosCombate

main()