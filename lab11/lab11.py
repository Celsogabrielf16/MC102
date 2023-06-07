from dataclasses import dataclass, field

def converteParaInt(lista: list) -> list[int]:
    listaFinal: list[int] = []
    for indice in range(len(lista)):
        listaFinal.append(lista[indice] if type(lista[indice]) == int else int(lista[indice]))
    return listaFinal

def converteListaParaTupla(lista: list[int]) -> tuple[int, int]:
    primeiroElemento: int = lista[0]
    segundoElemento: int = lista[1]
    return (primeiroElemento, segundoElemento)

def main() -> None:
    infoLink: list[int] = converteParaInt(input().split(' '))
    tamanhoMasmorra: list[int] = converteParaInt(input().split(' '))
    posicaoInicialLink: tuple[int, int] = converteListaParaTupla(converteParaInt(input().split(',')))
    posicaoFinalLink: tuple[int, int] = converteListaParaTupla(converteParaInt(input().split(',')))

    numeroMonstros: int = int(input())
    listaMonstros: list = []
    for indice in range(numeroMonstros):
        informacoesMonstro: list[str] = input().split(' ')
        vida: int = int(informacoesMonstro[0])
        dano: int = int(informacoesMonstro[1])
        tipo: str = informacoesMonstro[2]
        posicaoSeparada: list[str] = informacoesMonstro[3].split(',')
        posicao: tuple[int,int] = (int(posicaoSeparada[0]), int(posicaoSeparada[1]))
        listaMonstros.append(Monstro(indice, vida, dano, tipo, posicao))

    numeroObjetos: int = int(input())
    listaObjetos: list = []
    for indice in range(numeroObjetos):
        informacoesObjeto: list[str] = input().split(' ')
        nome: str = informacoesObjeto[0]
        tipo: str = informacoesObjeto[1]
        posicaoSeparada: list[str] = informacoesObjeto[2].split(',')
        posicao: tuple[int,int] = (int(posicaoSeparada[0]), int(posicaoSeparada[1]))
        status: int = int(informacoesObjeto[3])
        listaObjetos.append(Objeto(indice, nome, tipo, posicao, status))

    masmorra = Masmorra(tamanhoMasmorra[0], tamanhoMasmorra[1])
    
    link = Link(infoLink[0], infoLink[1], posicaoInicialLink)

    masmorra.init()
    masmorra.adicionaNaMatriz(posicaoInicialLink, 'P')
    masmorra.adicionaNaMatriz(posicaoFinalLink, '*')
    for monstro in listaMonstros:
        infoMonstro = monstro.getInformacoes()
        masmorra.adicionaNaMatriz(infoMonstro[4], infoMonstro[3])
    for objeto in listaObjetos:
        infoObjeto = objeto.getInformacoes()
        masmorra.adicionaNaMatriz(infoObjeto[3], infoObjeto[2])

    masmorra.mostraMatrizMasmorra()
    print(masmorra)
    print(link)
    print(listaMonstros)
    print(listaObjetos)

@dataclass
class Masmorra:
    numeroLinhas: int
    numeroColunas: int
    matrizMasmorra: list[str] = field(default_factory=list)

    def init(self):
        self._criaMatrizMasmorra()

    def _criaMatrizMasmorra(self) -> None:
        numeroTotalPosicoesMatriz: int = self.numeroLinhas * self.numeroColunas
        for _ in range(numeroTotalPosicoesMatriz):
            self.matrizMasmorra.append('.')

    def mostraMatrizMasmorra(self) -> None:
        for i in range(self.numeroLinhas):
            for j in range(self.numeroColunas):
                if j == self.numeroColunas - 1:
                    print(self.matrizMasmorra[i * self.numeroColunas + j], end="\n")
                else:
                    print(self.matrizMasmorra[i * self.numeroColunas + j], end=" ")

    def adicionaNaMatriz(self, posicao: tuple, elemento: str) -> None:
        posicaoK: int = self._posicaoIJParaK(posicao)
        self.matrizMasmorra[posicaoK] = elemento

    def _posicaoIJParaK(self, posicao: tuple) -> int:
        return self.numeroColunas * posicao[0] + posicao[1]

@dataclass
class Link:
    vida: int
    dano: int
    posicao: tuple[int, int]

    def imprime(self) -> None:
        print(self.vida, self.dano, self.posicao)

@dataclass
class Monstro:
    indice: int
    vida: int
    dano: int
    tipo: str
    posicao: tuple[int, int]

    def imprime(self) -> None:
        print(self.indice, self.vida, self.dano, self.tipo, self.posicao)

    def getInformacoes(self) -> list:
        return [self.indice, self.vida, self.dano, self.tipo, self.posicao]

@dataclass
class Objeto:
    indice: int
    nome: str
    tipo: str
    posicao: tuple[int, int]
    status: int

    def imprime(self) -> None:
        print(self.indice, self.nome, self.tipo, self.posicao, self.status)

    def getInformacoes(self) -> list:
        return [self.indice, self.nome, self.tipo, self.posicao, self.status]

""" def masmorra():
    link = Link(0)
    lista = []
    for j in range(3):
        lista.append(Monstro(j))
    for i in range(3):
        link.pri()
        for k in range(len(lista)):
            lista[k].pri()
    print(lista) """

if __name__ == '__main__':
    main()