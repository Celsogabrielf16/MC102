from dataclasses import dataclass

def main() -> None:
    quantidadeJogadores: int = int(input())
    listaJogadores: list = preencheListaJogadores(quantidadeJogadores)
    quantidadeJogadasAteDuvido: int = int(input())
    for jogador in listaJogadores:
        jogador._selectionSort()
        jogador.imprimeMao()

@dataclass
class Jogador:
    indice: int
    mao: list[str]
    forcaCartas: dict

    def imprimeMao(self) -> None:
        print(self.indice, self.mao)

    def _selectionSort(self):
        for indicePrimeiraCarta in range(len(self.mao) - 1):
            indiceCartaMaiorForca = indicePrimeiraCarta
            for indiceSegundaCarta in range(indicePrimeiraCarta + 1, len(self.mao), 1):
                forcaCartaMaiorForca: int = self.forcaCartas[self.mao[indiceCartaMaiorForca]]
                forcaSegundaCarta: int = self.forcaCartas[self.mao[indiceSegundaCarta]]
                if forcaCartaMaiorForca < forcaSegundaCarta:
                    indiceCartaMaiorForca = indiceSegundaCarta
            self.mao[indiceCartaMaiorForca], self.mao[indicePrimeiraCarta] = self.mao[indicePrimeiraCarta], self.mao[indiceCartaMaiorForca]

    def encontraForcaCarta(self, carta: str) -> int:
        return self.forcaCartas[carta]

def preencheListaJogadores(quantidadeJogadores: int) -> list:
    listaFinal: list = []
    dictForcaCartas: dict = criaDictForcaCartas()
    for indiceJogador in range(1, quantidadeJogadores + 1, 1):
        listaMao: list[str] = input().split(', ')
        listaFinal.append(Jogador(indiceJogador, listaMao, dictForcaCartas))
    return listaFinal

def criaDictForcaCartas() -> dict:
    listaCartas: list[str] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    listaNaipes: list[str] = ['O', 'E', 'C', 'P']
    dicionarioOrdemCartas: dict = dict()
    for carta in listaCartas:
        for naipe in listaNaipes:
            cartaComNaipe: str = carta + naipe
            forcaCarta: int = encontraIndice(listaCartas, carta) * 4 + encontraIndice(listaNaipes, naipe) + 1
            dicionarioOrdemCartas[cartaComNaipe] = forcaCarta
    return dicionarioOrdemCartas

def encontraIndice(lista: list[str], elemento: str) -> int:
    for i in range(len(lista)):
        if lista[i] == elemento:
            return i
    return -1


if __name__ == '__main__':
    main()