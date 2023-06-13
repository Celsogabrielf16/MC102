from dataclasses import dataclass


# Recebe uma lista de strings e retorna uma list de inteiros
def converteParaInt(lista: list) -> list[int]:
    listaFinal: list[int] = []
    for indice in range(len(lista)):
        listaFinal.append(lista[indice] if type(lista[indice]) == int else int(lista[indice]))
    return listaFinal


# Recebe uma lista com dois inteiros e retorna um tupla de inteiros
def converteListaParaTupla(lista: list[int]) -> tuple[int, int]:
    primeiroElemento: int = lista[0]
    segundoElemento: int = lista[1]
    return (primeiroElemento, segundoElemento)


# Rebe o numero de monstros totais e cria um monstro do tipo Monstro e o adiciona em uma lista, ao final retorna essa lista de monstros
def preencheListaMonstros(numeroMonstros: int, tamanhoMasmorra: list[int]) -> list:
    listaFinal: list = []
    for indice in range(numeroMonstros):
        informacoesMonstro: list[str] = input().split(' ')
        vida: int = int(informacoesMonstro[0])
        dano: int = int(informacoesMonstro[1])
        tipo: str = informacoesMonstro[2]
        posicaoSeparada: list[str] = informacoesMonstro[3].split(',')
        posicao: tuple[int, int] = (int(posicaoSeparada[0]), int(posicaoSeparada[1]))
        listaFinal.append(Monstro(indice, vida, dano, tipo, posicao, tamanhoMasmorra))
    return listaFinal


# Rebe o numero de objetos totais e cria um objeto do tipo Objeto e o adiciona em uma lista, ao final retorna essa lista de objetos
def preencheListaObjetos(numeroObjetos: int) -> list:
    listaFinal: list = []
    for indice in range(numeroObjetos):
        informacoesObjeto: list[str] = input().split(' ')
        nome: str = informacoesObjeto[0]
        tipo: str = informacoesObjeto[1]
        posicaoSeparada: list[str] = informacoesObjeto[2].split(',')
        posicao: tuple[int, int] = (int(posicaoSeparada[0]), int(posicaoSeparada[1]))
        status: int = int(informacoesObjeto[3])
        listaFinal.append(Objeto(indice, nome, tipo, posicao, status))
    return listaFinal


# Cria a masmorra e adiciona nela todos os elementos presentes em suas respectivas posicoes
def criaMasmorraInicial(masmorra, posicaoInicialLink: tuple, posicaoFinalLink: tuple, listaMonstros: list, listaObjetos: list) -> None:
    masmorra.init()
    for objeto in listaObjetos:
        masmorra.adicionaNaMatriz(objeto.getPosicao(), objeto.getTipo())
    for monstro in listaMonstros:
        masmorra.adicionaNaMatriz(monstro.getPosicao(), monstro.getTipo())
    masmorra.adicionaNaMatriz(posicaoInicialLink, 'P')
    masmorra.adicionaNaMatriz(posicaoFinalLink, '*')


# Adiciona novamente os objetos na matriz caso ela tenha sido sobreposta, e retorna uma lista com as posicoes dos objetos restantes
def adicionaObjetosNaMatriz(masmorra, listaObjetos: list) -> list[tuple]:
    listaFinal: list[tuple] = []
    for objeto in listaObjetos:
        listaFinal.append(objeto.getPosicao())
        masmorra.adicionaNaMatriz(objeto.getPosicao(), objeto.getTipo())
    return listaFinal


# Move o monstro para a sua proxima posicao de acordo com seu tipo
def movimentaMonstro(listaPosicoesOcupadasObjetos: list[tuple], listaMonstros: list, masmorra) -> None:
    listaPosicoesOcupadasAnteriormente: list[tuple] = []
    listaPosicoesOcupadas: list[tuple] = []
    # Loop percorrendo os monstros, e adicionando sua posição anterior numa lista, move o monstro e adiciona sua nova posicao em uma lista
    for monstro in listaMonstros:
        listaPosicoesOcupadasAnteriormente.append(monstro.getPosicao())
        masmorra.atualizaMatrizMonstro(monstro)
        listaPosicoesOcupadas.append(monstro.getPosicao())
    # Loop percorrendo as posicoes anteriores dos monstros
    for posicao in listaPosicoesOcupadasAnteriormente:
        # Se a posicao anterior do monstros não foi ocupada por outro monstro ou não havia algum objeto nela, substitui essa posicao anterior por '.'
        if posicao not in listaPosicoesOcupadas and posicao not in listaPosicoesOcupadasObjetos:
            masmorra.adicionaNaMatriz(posicao, '.')


def main() -> None:
    # Recebe as informações dadas
    infoLink: list[int] = converteParaInt(input().split(' '))
    tamanhoMasmorra: list[int] = converteParaInt(input().split(' '))
    posicaoInicialLink: tuple[int, int] = converteListaParaTupla(converteParaInt(input().split(',')))
    posicaoFinalLink: tuple[int, int] = converteListaParaTupla(converteParaInt(input().split(',')))
    numeroMonstros: int = int(input())
    listaMonstros: list = preencheListaMonstros(numeroMonstros, tamanhoMasmorra)
    numeroObjetos: int = int(input())
    listaObjetos: list = preencheListaObjetos(numeroObjetos)

    # Cria a classe Masmorra e a do Link, a classe Monstro e Objeto foram criada anteriormente
    masmorra = Masmorra(tamanhoMasmorra[0], tamanhoMasmorra[1], list())
    link = Link(infoLink[0], infoLink[1], posicaoInicialLink, tamanhoMasmorra)

    criaMasmorraInicial(masmorra, posicaoInicialLink, posicaoFinalLink, listaMonstros, listaObjetos)

    # Loop, que pode ser visto como cada 'Frame' da masmorra
    rodaLoop = True
    while rodaLoop:
        masmorra.mostraMatrizMasmorra()

        listaPosicoesOcupadasObjetos: list[tuple] = adicionaObjetosNaMatriz(masmorra, listaObjetos)
        movimentaMonstro(listaPosicoesOcupadasObjetos, listaMonstros, masmorra)

        # Reescreve o '*' pois tem prioridade de exibição em relação aos monstros e objetos
        masmorra.adicionaNaMatriz(posicaoFinalLink, '*')

        # Move o link de acordo com seu proximo movimento
        masmorra.atualizaMatrizLink(link)

        # Se Link chegou a saida da masmorra encerra o programa
        if link.getPosicao() == posicaoFinalLink:
            rodaLoop = False
            masmorra.mostraMatrizMasmorra()
            print('Chegou ao fim!')

        resultadoEscaneamento: list = escaneaMasmorra(link.getPosicao(), listaMonstros, listaObjetos)
        if resultadoEscaneamento[0] and rodaLoop:
            # Percorre a lista do que foi encontrado e verifica se é um objeto ou um monstro
            for resultado in resultadoEscaneamento[1]:
                if resultado in listaObjetos:
                    rodaLoop = encontrouObjeto(listaObjetos, resultado, link, masmorra)

                if resultado in listaMonstros:
                    rodaLoop = encontrouMonstro(listaMonstros, resultado, link, masmorra)

                # Caso ele tenha morrido ao pegra um objeto de dano ou morrido em batalha para o programa
                if rodaLoop is False:
                    break


# Executa as ações necessarias quando Link encontra um monstro em sua nova posção
def encontrouMonstro(listaMonstros: list, monstro, link, masmorra):
    indiceMonstro: int = listaMonstros.index(monstro)
    danoLink: int = link.getDano()
    vidaMonstro: int = monstro.atualizaVida(-danoLink)

    # Como caso o dano exeda a vida do monstro queremos exibir apenas o dano necessario para mata-lo:
    if vidaMonstro <= 0:
        danoLink += vidaMonstro
    print(f'O Personagem deu {danoLink} de dano ao monstro na posicao {monstro.getPosicao()}')
    vidaLink: int = link.getVida()

    # Se o monstro sobreviver ao ataque do link:
    if vidaMonstro > 0:
        danoMonstro: int = monstro.getDano()

        # Se o dano dado pelo monstro for maior ou igual a vida de link, e queremos exibir apenas o dano necessario para mata-lo:
        if vidaLink - danoMonstro <= 0:
            danoMonstro = vidaLink
        vidaLink = link.atualizaVida(-danoMonstro)
        print(f'O Monstro deu {danoMonstro} de dano ao Personagem. Vida restante = {vidaLink}')

    # Se o monstro for derrotado pelo Link tiramos ele da lista dos monstro pra que não seja mais exibido, e exibimos o 'P' no local da batalha
    if vidaMonstro <= 0:
        masmorra.adicionaNaMatriz(monstro.getPosicao(), 'P')
        del listaMonstros[indiceMonstro]

    # Se o Link morrer na batalha colocamos um 'X' no local da batalha e encerramos o programa, senão continua executando para o proximo 'Frame'
    if vidaLink <= 0:
        masmorra.adicionaNaMatriz(monstro.getPosicao(), 'X')
        masmorra.mostraMatrizMasmorra()
        return False
    else:
        return True


# Executa as ações necessarias quando Link encontra um objeto em sua nova posção
def encontrouObjeto(listaObjetos: list, objeto, link, masmorra) -> bool:
    indiceObjeto: int = listaObjetos.index(objeto)
    infoObjeto: list = objeto.getInformacoes()
    continuaVivo: bool = True
    # Se for um objeto de vida (v)
    if infoObjeto[2] == 'v':
        # Atualiza a vida do Link e caso ele morra coloca um X
        if link.atualizaVida(infoObjeto[4]) <= 0:
            masmorra.adicionaNaMatriz(infoObjeto[3], 'X')
            masmorra.mostraMatrizMasmorra()
            continuaVivo = False
    # Se for um objeto de dano (d)
    else:
        link.atualizaDano(infoObjeto[4])
    # Como ele coletou o objeto tira da lista de objetos para não ser mais exibido
    del listaObjetos[indiceObjeto]
    print(f'[{infoObjeto[2]}]Personagem adquiriu o objeto {infoObjeto[1]} com status de {infoObjeto[4]}')
    return continuaVivo


# Verifica a posição do link, caso tenha algo na mesma posição ele retorna True, e uma lista com o que foi encontrado
def escaneaMasmorra(posicaoLink: tuple[int, int], listaMonstros: list, listaObjetos: list) -> list:
    listaFinal: list = []
    for objeto in listaObjetos:
        if objeto.getPosicao() == posicaoLink:
            listaFinal.append(objeto)
    for monstro in listaMonstros:
        if monstro.getPosicao() == posicaoLink:
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

    # inicia a Classe Masmorra
    def init(self) -> None:
        self._criaMatrizMasmorra()

    # Cria uma lista de '.'
    def _criaMatrizMasmorra(self) -> None:
        numeroTotalPosicoesMatriz: int = self.numeroLinhas * self.numeroColunas
        for _ in range(numeroTotalPosicoesMatriz):
            self.matrizMasmorra.append('.')

    # Imprime a matriz masmorra
    def mostraMatrizMasmorra(self) -> None:
        for i in range(self.numeroLinhas):
            for j in range(self.numeroColunas):
                if j == self.numeroColunas - 1:
                    print(self.matrizMasmorra[i * self.numeroColunas + j], end="\n")
                else:
                    print(self.matrizMasmorra[i * self.numeroColunas + j], end=" ")
        print()

    # Adiciona o elemento desejado na posição indicada
    def adicionaNaMatriz(self, posicao: tuple, elemento: str) -> None:
        posicaoK: int = self._posicaoIJParaK(posicao)
        self.matrizMasmorra[posicaoK] = elemento

    # Atualiza a matriz masmorra apos o movimento do link
    def atualizaMatrizLink(self, link) -> None:
        posicaoAnteriorK: int = self._posicaoIJParaK(link.getPosicao())
        posicaoK: int = self._posicaoIJParaK(link.andar())
        if self.matrizMasmorra[posicaoAnteriorK] == 'P':
            self.matrizMasmorra[posicaoAnteriorK] = '.'
        self.matrizMasmorra[posicaoK] = 'P'

    # Atualiza a matriz masmorra apos o movimento do monstro
    def atualizaMatrizMonstro(self, monstro) -> None:
        posicaoK: int = self._posicaoIJParaK(monstro.andar())
        self.matrizMasmorra[posicaoK] = monstro.getTipo()

    # Recebe uma tupla I J, retorna um indice K correspondente
    def _posicaoIJParaK(self, posicao: tuple) -> int:
        return self.numeroColunas * posicao[0] + posicao[1]


@dataclass
class Link:
    vida: int
    dano: int
    posicao: tuple[int, int]
    tamanhoMasmorra: list[int]
    amaldicoado: bool = True

    def getPosicao(self) -> tuple[int, int]:
        return self.posicao

    def getDano(self) -> int:
        return self.dano

    def getVida(self) -> int:
        return self.vida

    # Atualiza a vida do Link de acordo com o status, que pode ser tanto o de um objeto de vida e dano quanto o dano de um monstro
    def atualizaVida(self, status: int) -> int:
        self.vida += status
        return self.vida

    # Atualiza o dano do Link de acordo com o status do objeto dano
    def atualizaDano(self, status: int) -> int:
        novoDano: int = self.dano + status
        if novoDano >= 1:
            self.dano = novoDano
            return self.dano
        else:
            self.dano = 1
            return self.dano

    # Define qual sera a nova posicao do Link
    def andar(self) -> tuple:
        # Se ela ainda estiver amaldicoado ele deve ir para a linha de baixo
        if self.amaldicoado:
            self.posicao = self.posicao[0] + 1, self.posicao[1]
            if self.posicao[0] == self.tamanhoMasmorra[0] - 1:
                self.amaldicoado = False
            return self.posicao
        else:
            # Se ele estiver em uma linha par e não estiver na primeira coluna ele vai para a esquerda
            if self.posicao[0] % 2 == 0 and self.posicao[1] != 0:
                self.posicao = self.posicao[0], self.posicao[1] - 1
                return self.posicao
            # Se ele estiver em uma linha impar e não estiver na ultima coluna ele vai para a direira
            elif self.posicao[0] % 2 != 0 and self.posicao[1] != self.tamanhoMasmorra[1] - 1:
                self.posicao = self.posicao[0], self.posicao[1] + 1
                return self.posicao
            # Se não entrar em um dos casos anteriores significa que ele so pode ir para cima
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

    def getDano(self) -> int:
        return self.dano

    def getTipo(self) -> str:
        return self.tipo

    def getPosicao(self) -> tuple:
        return self.posicao

    # Atualiza a vida do monstro de acordo com o dano do Link
    def atualizaVida(self, status: int) -> int:
        self.vida += status
        return self.vida

    # Retorna a nova posicao do monstro
    def andar(self) -> tuple[int, int]:
        self.posicao = self.proximaPosicao()
        return self.posicao

    # Determina e retorna a nova posicao do monstro de acordo com seu tipo
    def proximaPosicao(self) -> tuple[int, int]:
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

    def getInformacoes(self) -> list:
        return [self.indice, self.nome, self.tipo, self.posicao, self.status]

    def getTipo(self) -> str:
        return self.tipo

    def getPosicao(self) -> tuple[int, int]:
        return self.posicao


if __name__ == '__main__':
    main()
