from dataclasses import dataclass


@dataclass
class Jogador:
    indiceJogador: int
    maoJogador: list[str]
    forcaCartas: dict[str, int]
    listaCartasJogadas: list[str]
    numeroCartasJogadas: int = 0

    def imprimeMao(self) -> None:
        self._ordenacaoPorSelecao()
        print(f'Jogador {self.indiceJogador}')
        print('Mão:', end='')
        for indiceCarta in range(len(self.maoJogador)):
            print(f' {self.maoJogador[indiceCarta]}', end='')
        print()

    # Adiciona a pilha de descarte na mao do jogador
    def adicionaPilhaNaMao(self, pilha: list[str]) -> None:
        for carta in pilha:
            self.maoJogador.append(carta)

    # Verefica se ainda restam cartas na mão do jogador
    def acabouCartasJogador(self) -> bool:
        if len(self.maoJogador) == 0:
            return True
        else:
            return False

    def jogada(self, pilha: list[str], ultimaCartaDescartada: str) -> list:
        cartaDescartada: str = ''
        blefou: bool = False

        # Como a mao esta na ordem decrescente, se a pliha estiver vazia o jogador deve jogar suas ultimas cartas de mesmo numero/letra
        if len(pilha) == 0:
            self._buscaCartasIguais(self.maoJogador[len(self.maoJogador) - 1])
            cartaDescartada = self.maoJogador[len(self.maoJogador) - 1][:-1]
        else:
            self._buscaCartasIguais(ultimaCartaDescartada + 'O')
            # Se tiver cartas da mesma letra/numero da ultima carta descartada na mao do jogador ele deve jogar elas
            if len(self.listaCartasJogadas) != 0:
                cartaDescartada = self.listaCartasJogadas[0][:-1]
            else:
                # Encontrar a menor carta posssivel maior que a carta do ultimo descarte
                encontrouCartaMaiorForca: bool = False
                for indiceCarta in range(len(self.maoJogador) - 1, -1, -1):
                    forcaUltimaCartaDescartada: int = self.forcaCartas[ultimaCartaDescartada + 'P']
                    if forcaUltimaCartaDescartada < self.forcaCartas[self.maoJogador[indiceCarta]]:
                        self._buscaCartasIguais(self.maoJogador[indiceCarta])
                        cartaDescartada = self.maoJogador[indiceCarta][:-1]
                        encontrouCartaMaiorForca = True
                        break
                # Se não encontrou nenhuma carta maior que a do ultimo descarte, o jogador deve blefar
                if encontrouCartaMaiorForca is not True:
                    self._buscaCartasIguais(self.maoJogador[len(self.maoJogador) - 1])
                    cartaDescartada = ultimaCartaDescartada
                    blefou = True
        print(f'[Jogador {self.indiceJogador}] {self.numeroCartasJogadas} carta(s) {cartaDescartada}')
        self._descartaCarta()
        return [self.listaCartasJogadas, cartaDescartada, blefou]

    # Tira da mao do jogador a(s) carta(s) descartada(s)
    def _descartaCarta(self) -> None:
        for cartaDescartada in self.listaCartasJogadas:
            for cartaMao in self.maoJogador:
                if cartaMao == cartaDescartada:
                    indiceCarta: int = self._encontraIndice(cartaMao)
                    del self.maoJogador[indiceCarta]

    # Busca cartas com mesmo número/letra da carta dada como parametro na mao do jogador
    def _buscaCartasIguais(self, carta: str) -> None:
        self.numeroCartasJogadas = 0
        forcaCartaOuro: int = self._determinaForcaCartaOuro(carta)
        self.listaCartasJogadas = []
        for indice in range(4):
            indiceCarta: int = self._buscaBinariaPorForca(forcaCartaOuro + indice)
            if indiceCarta != -1:
                self.listaCartasJogadas.append(self.maoJogador[indiceCarta])
                self.numeroCartasJogadas += 1

    # Ordena a mao do jogador de acordo com a força da carta
    def _ordenacaoPorSelecao(self) -> None:
        for indicePrimeiraCarta in range(len(self.maoJogador) - 1):
            indiceCartaMaiorForca = indicePrimeiraCarta
            for indiceSegundaCarta in range(indicePrimeiraCarta + 1, len(self.maoJogador), 1):
                forcaCartaMaiorForca: int = self.forcaCartas[self.maoJogador[indiceCartaMaiorForca]]
                forcaSegundaCarta: int = self.forcaCartas[self.maoJogador[indiceSegundaCarta]]
                if forcaCartaMaiorForca < forcaSegundaCarta:
                    indiceCartaMaiorForca = indiceSegundaCarta
            auxiliar = self.maoJogador[indicePrimeiraCarta]
            self.maoJogador[indicePrimeiraCarta] = self.maoJogador[indiceCartaMaiorForca]
            self.maoJogador[indiceCartaMaiorForca] = auxiliar

    # Faz a busca do elemento com a forca desejado na mao do jogador, e retorna o indice do mesmo
    def _buscaBinariaPorForca(self, forcaElemento: int) -> int:
        esquerda: int = 0
        direita: int = len(self.maoJogador) - 1
        while esquerda <= direita:
            meio: int = (esquerda + direita) // 2
            if self.forcaCartas[self.maoJogador[meio]] == forcaElemento:
                return meio
            elif self.forcaCartas[self.maoJogador[meio]] > forcaElemento:
                esquerda = meio + 1
            else:
                direita = meio - 1
        return -1

    # Encontra a forca da carta mais fraca daquela letra/numero, ou seja sua carta ouro
    def _determinaForcaCartaOuro(self, carta: str) -> int:
        for chave, valor in self.forcaCartas.items():
            if carta[:-1] == chave[:-1]:
                return valor
        return -1

    # Encontra o indice da carta desejada
    def _encontraIndice(self, carta: str) -> int:
        for i in range(len(self.maoJogador)):
            if self.maoJogador[i] == carta:
                return i
        return -1


def main() -> None:
    dictForcaCartas, listaCartas = forcaCartas()
    quantidadeJogadores: int = int(input())
    listaJogadores: list = preencheListaJogadores(quantidadeJogadores, dictForcaCartas, listaCartas)
    quantidadeJogadasAteDuvido: int = int(input())

    jogoAcabou = False
    primeiroJogadorDaRodada: int = 0
    while jogoAcabou is not True:
        informacoesRodada: list = rodada(listaJogadores, quantidadeJogadores, quantidadeJogadasAteDuvido, jogoAcabou, primeiroJogadorDaRodada)
        quantidadeJogadasAteDuvido, jogoAcabou, primeiroJogadorDaRodada = informacoesRodada


def rodada(listaJogadores: list, quantidadeJogadores: int, quantidadeJogadasAteDuvido: int, jogoAcabou: bool, primeiroJogadorDaRodada: int) -> list:
    pilhaDescarte: list[str] = []
    ultimaCartaDescartada: str = ''
    blefou: bool = False
    indiceUltimoJogadorAJogar: int = 0

    for jogador in listaJogadores:
        jogador.imprimeMao()
    imprimePilha(pilhaDescarte)

    # Jogada de todos os jogadores até algum jogador duvidar
    for indiceJogador in range(primeiroJogadorDaRodada, quantidadeJogadasAteDuvido, 1):
        vaiSerQuestionado: bool = False
        # Se o jogador for o qual vai ser questionados ele não pode ganhar antes de ser questionado, caso acabe suas cartas
        if indiceJogador == quantidadeJogadasAteDuvido - 1:
            vaiSerQuestionado = True

        if indiceJogador >= quantidadeJogadores:
            indiceJogador = indiceJogador % quantidadeJogadores

        # Jogador efetua sua jogada e retorna algumas informações
        informacoesJogada = listaJogadores[indiceJogador].jogada(pilhaDescarte, ultimaCartaDescartada)
        ultimaCartaDescartada = informacoesJogada[1]
        blefou = informacoesJogada[2]

        # imprime a pilha de descarte apos a jogada
        for carta in informacoesJogada[0]:
            pilhaDescarte.append(carta)
        imprimePilha(pilhaDescarte)

        # Caso tenha acabado as cartas do jogador e ele não vai ser questionado ele ganhou o jogo
        if listaJogadores[indiceJogador].acabouCartasJogador() is True and vaiSerQuestionado is not True:
            jogoAcabou = True
            print(f'Jogador {indiceJogador + 1} é o vencedor!')
            break

        indiceUltimoJogadorAJogar = indiceJogador

    # Aqui executamos as ações necesssarias quando um jogador duvida do outro
    indiceJogadorDuvidou: int = quantidadeJogadasAteDuvido % quantidadeJogadores
    if jogoAcabou is not True:
        print(f'Jogador {indiceJogadorDuvidou + 1} duvidou.')
        # Se o jogador questionado blefou ele fica com toda a pilha
        if blefou is True:
            listaJogadores[indiceUltimoJogadorAJogar].adicionaPilhaNaMao(pilhaDescarte)
            pilhaDescarte = []
        else:
            # Se ele não blefou fica com as cartes quem duvidou
            listaJogadores[indiceJogadorDuvidou].adicionaPilhaNaMao(pilhaDescarte)
            pilhaDescarte = []
            # Caso tenha acabado as cartas do jogador questionado ele ganhou o jogo
            if listaJogadores[indiceUltimoJogadorAJogar].acabouCartasJogador() is True:
                for jogador in listaJogadores:
                    jogador.imprimeMao()
                imprimePilha(pilhaDescarte)
                print(f'Jogador {indiceUltimoJogadorAJogar + 1} é o vencedor!')
                jogoAcabou = True

    # Aqui regularizamos o intervalo do proximo for, para que comece apartir do jogador que duvidou, e não do jogador 1
    quantidadeJogadasAteDuvido -= primeiroJogadorDaRodada
    primeiroJogadorDaRodada = indiceJogadorDuvidou
    quantidadeJogadasAteDuvido += primeiroJogadorDaRodada

    return [quantidadeJogadasAteDuvido, jogoAcabou, primeiroJogadorDaRodada]


def imprimePilha(pilha: list) -> None:
    print('Pilha:', end='')
    for indice in range(len(pilha)):
        print(f' {pilha[indice]}', end='')
    print()


# Cria uma lista com todos os jogadores
def preencheListaJogadores(quantidadeJogadores: int, dictForcaCartas: dict, listaCartas: list) -> list:
    listaFinal: list = []
    for indiceJogador in range(1, quantidadeJogadores + 1, 1):
        listaMao: list[str] = input().split(', ')
        listaFinal.append(Jogador(indiceJogador, listaMao, dictForcaCartas, list()))
    return listaFinal


# Cria um dicionario com todas as cartas e suas respectivas forças com a finalidade de facilitar a ordenação posteriormente
def forcaCartas() -> tuple[dict, list]:
    listaCartas: list[str] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    listaNaipes: list[str] = ['O', 'E', 'C', 'P']
    dicionarioForcaCartas: dict = dict()
    for carta in listaCartas:
        for naipe in listaNaipes:
            cartaComNaipe: str = carta + naipe
            forcaCarta: int = encontraIndice(listaCartas, carta) * 4 + encontraIndice(listaNaipes, naipe) + 1
            dicionarioForcaCartas[cartaComNaipe] = forcaCarta
    return dicionarioForcaCartas, listaCartas


# Encontra o indice do elemento desejado na lista dada
def encontraIndice(lista: list[str], elemento: str) -> int:
    for i in range(len(lista)):
        if lista[i] == elemento:
            return i
    return -1


if __name__ == '__main__':
    main()
