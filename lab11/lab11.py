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

def preencheListaMonstros(numeroMonstros: int, tamanhoMasmorra: list[int]) -> list:
    listaFinal: list = []
    for indice in range(numeroMonstros):
        informacoesMonstro: list[str] = input().split(' ')
        vida: int = int(informacoesMonstro[0])
        dano: int = int(informacoesMonstro[1])
        tipo: str = informacoesMonstro[2]
        posicaoSeparada: list[str] = informacoesMonstro[3].split(',')
        posicao: tuple[int,int] = (int(posicaoSeparada[0]), int(posicaoSeparada[1]))
        listaFinal.append(Monstro(indice, vida, dano, tipo, posicao, tamanhoMasmorra))
    return listaFinal

def preencheListaObjetos(numeroObjetos: int) -> list:
    listaFinal: list = []
    for indice in range(numeroObjetos):
        informacoesObjeto: list[str] = input().split(' ')
        nome: str = informacoesObjeto[0]
        tipo: str = informacoesObjeto[1]
        posicaoSeparada: list[str] = informacoesObjeto[2].split(',')
        posicao: tuple[int,int] = (int(posicaoSeparada[0]), int(posicaoSeparada[1]))
        status: int = int(informacoesObjeto[3])
        listaFinal.append(Objeto(indice, nome, tipo, posicao, status))
    return listaFinal

def criaMasmorraInicial(masmorra, posicaoInicialLink, posicaoFinalLink, listaMonstros, listaObjetos) -> None:
    masmorra.init()
    for objeto in listaObjetos:
        infoObjeto = objeto.getInformacoes()
        masmorra.adicionaNaMatriz(infoObjeto[3], infoObjeto[2])
    for monstro in listaMonstros:
        infoMonstro = monstro.getInformacoes()
        masmorra.adicionaNaMatriz(infoMonstro[4], infoMonstro[3])
    masmorra.adicionaNaMatriz(posicaoInicialLink, 'P')
    masmorra.adicionaNaMatriz(posicaoFinalLink, '*')

def main() -> None:
    infoLink: list[int] = converteParaInt(input().split(' '))
    tamanhoMasmorra: list[int] = converteParaInt(input().split(' '))
    posicaoInicialLink: tuple[int, int] = converteListaParaTupla(converteParaInt(input().split(',')))
    posicaoFinalLink: tuple[int, int] = converteListaParaTupla(converteParaInt(input().split(',')))

    numeroMonstros: int = int(input())
    listaMonstros: list = preencheListaMonstros(numeroMonstros, tamanhoMasmorra)
    
    numeroObjetos: int = int(input())
    listaObjetos: list = preencheListaObjetos(numeroObjetos)
    
    masmorra = Masmorra(tamanhoMasmorra[0], tamanhoMasmorra[1], list())
    
    link = Link(infoLink[0], infoLink[1], posicaoInicialLink, tamanhoMasmorra)

    criaMasmorraInicial(masmorra, posicaoInicialLink, posicaoFinalLink, listaMonstros, listaObjetos)

    rodaLoop = True

    while rodaLoop:
        masmorra.mostraMatrizMasmorra()

        listaPosicoesOcupadasObjetos: list[tuple] = []
        for objeto in listaObjetos:
            infoObjeto = objeto.getInformacoes()
            listaPosicoesOcupadasObjetos.append(infoObjeto[3])
            masmorra.adicionaNaMatriz(infoObjeto[3], infoObjeto[2])

        listaPosicoesOcupadasAnteriormente: list[tuple] = []
        listaPosicoesOcupadas: list[tuple] = []
        for monstro in listaMonstros:
            listaPosicoesOcupadasAnteriormente.append(monstro.getPosicao())
            masmorra.atualizaMatriz(monstro)
            listaPosicoesOcupadas.append(monstro.getPosicao())
        for posicao in listaPosicoesOcupadasAnteriormente:
            if posicao not in listaPosicoesOcupadas and posicao not in listaPosicoesOcupadasObjetos:
                masmorra.adicionaNaMatriz(posicao, '.')

        masmorra.adicionaNaMatriz(posicaoFinalLink, '*')
        masmorra.atualizaMatrizLink(link.getPosicao(), link.andar())

        if link.getPosicao() == posicaoFinalLink:
            rodaLoop = False
            masmorra.mostraMatrizMasmorra()
            print('Chegou ao fim!')

        resultadoEscaneamento: list = escaneaMasmorra(link.getPosicao(), listaMonstros, listaObjetos)
        if resultadoEscaneamento[0] and rodaLoop:
            for resultado in resultadoEscaneamento[1]:
                if resultado in listaObjetos:
                    indiceObjeto: int = listaObjetos.index(resultado)
                    infoObjeto: list = resultado.getInformacoes()
                    if infoObjeto[2] == 'v':
                        if link.atualizaVida(infoObjeto[4]) <= 0:
                            masmorra.adicionaNaMatriz(infoObjeto[3], 'X')
                            masmorra.mostraMatrizMasmorra()
                    else:
                        link.atualizaDano(infoObjeto[4])
                    del listaObjetos[indiceObjeto]
                    print(f'[{infoObjeto[2]}]Personagem adquiriu o objeto {infoObjeto[1]} com status de {infoObjeto[4]}')
                    
                if resultado in listaMonstros:
                    indiceMonstro = listaMonstros.index(resultado)
                    infoMonstro: list = resultado.getInformacoes()

                    danoLink: int = link.getDano()
                    vidaMonstro: int = resultado.atualizaVida(-danoLink)
                    if vidaMonstro <= 0:
                        danoLink += vidaMonstro
                    print(f'O Personagem deu {danoLink} de dano ao monstro na posicao {infoMonstro[4]}')
                    

                    vidaLink: int = link.getVida()
                    if vidaMonstro > 0:
                        danoMonstro: int = infoMonstro[2]
                        if vidaLink - danoMonstro <= 0:
                            danoMonstro = vidaLink
                        vidaLink = link.atualizaVida(-danoMonstro)
                        print(f'O Monstro deu {danoMonstro} de dano ao Personagem. Vida restante = {vidaLink}')

                    if vidaMonstro <= 0:
                        masmorra.adicionaNaMatriz(infoMonstro[4], 'P')
                        del listaMonstros[indiceMonstro]
                        
                    if vidaLink <= 0:
                        masmorra.adicionaNaMatriz(infoMonstro[4], 'X')
                        masmorra.mostraMatrizMasmorra() 
                        rodaLoop = False
                        break



def escaneaMasmorra(posicaoLink: tuple[int,int], listaMonstros: list, listaObjetos: list) -> list:
    listaFinal: list = []
    for objeto in listaObjetos:
        infoObjetos = objeto.getInformacoes()
        if infoObjetos[3] == posicaoLink:
            listaFinal.append(objeto)
    for monstro in listaMonstros:
        infoMonstro = monstro.getInformacoes()
        if infoMonstro[4] == posicaoLink:
            listaFinal.append(monstro)
    if len(listaFinal) != 0:
        return [True, listaFinal]
    else: 
        return [False]


@dataclass
class Masmorra:
    numeroLinhas: int
    numeroColunas: int
    matrizMasmorra: list[str]

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
        print()

    def adicionaNaMatriz(self, posicao: tuple, elemento: str) -> None:
        posicaoK: int = self._posicaoIJParaK(posicao)
        self.matrizMasmorra[posicaoK] = elemento

    def atualizaMatrizLink(self, posicaoAnterior: tuple, posicao: tuple) -> None:
        posicaoAnteriorK: int = self._posicaoIJParaK(posicaoAnterior)
        posicaoK: int = self._posicaoIJParaK(posicao)
        if self.matrizMasmorra[posicaoAnteriorK] == 'P':
            self.matrizMasmorra[posicaoAnteriorK] = '.'
        self.matrizMasmorra[posicaoK] = 'P'

    def atualizaMatriz(self, monstro) -> None:
        infoMonstro = monstro.getInformacoes()
        posicaoK: int = self._posicaoIJParaK(monstro.andar())
        self.matrizMasmorra[posicaoK] = infoMonstro[3]


    def _posicaoIJParaK(self, posicao: tuple) -> int:
        return self.numeroColunas * posicao[0] + posicao[1]

@dataclass
class Link:
    vida: int
    dano: int
    posicao: tuple[int, int]
    tamanhoMasmorra: list[int]
    amaldicoado: bool = True

    def imprime(self) -> None:
        print(self.vida, self.dano, self.posicao)

    def getPosicao(self) -> tuple:
        return self.posicao
    
    def getDano(self) -> int:
        return self.dano
    
    def getVida(self) -> int:
        return self.vida
    
    def atualizaVida(self, status: int) -> int:
        self.vida += status
        return self.vida
    
    def atualizaDano(self, status: int) -> int:
        novoDano: int = self.dano + status
        if novoDano >= 1:
            self.dano = novoDano
            return self.dano
        else:
            self.dano = 1
            return self.dano
    
    def andar(self) -> tuple:
        if self.amaldicoado:
            self.posicao = self.posicao[0] + 1, self.posicao[1]
            if self.posicao[0] == self.tamanhoMasmorra[0] - 1:
                self.amaldicoado = False
            return self.posicao
        else:
            if self.posicao[0] % 2 == 0 and self.posicao[1] != 0:
                self.posicao = self.posicao[0], self.posicao[1] - 1
                return self.posicao
            elif self.posicao[0] % 2 != 0 and self.posicao[1] != self.tamanhoMasmorra[1] - 1:
                self.posicao = self.posicao[0], self.posicao[1] + 1
                return self.posicao
            else:
                self.posicao = self.posicao[0] - 1, self.posicao[1]
                return self.posicao

@dataclass
class Monstro:
    indice: int
    vida: int
    dano: int
    tipo: str
    posicao: tuple[int, int]
    tamanhoMasmorra: list[int]

    def imprime(self) -> None:
        print(self.indice, self.vida, self.dano, self.tipo, self.posicao)

    def getInformacoes(self) -> list:
        return [self.indice, self.vida, self.dano, self.tipo, self.posicao]
    
    def getPosicao(self) -> tuple:
        return self.posicao
    
    def atualizaVida(self, status: int) -> int:
        self.vida += status
        return self.vida
    
    def andar(self) -> tuple:
        self.posicao = self.proximaPosicao()
        return self.posicao
    
    def proximaPosicao(self) -> tuple:
        match self.tipo:
            case 'U':
                if self.posicao[0] > 0:
                    return self.posicao[0] - 1, self.posicao[1]
            case 'D':
                if self.posicao[0] < self.tamanhoMasmorra[0] - 1:
                    return self.posicao[0] + 1, self.posicao[1]
            case 'L':
                if self.posicao[1] > 0:
                    return self.posicao[0], self.posicao[1] - 1
            case 'R':
                if self.posicao[1] < self.tamanhoMasmorra[1] - 1:
                    return self.posicao[0], self.posicao[1] + 1
        return self.posicao

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


if __name__ == '__main__':
    main()