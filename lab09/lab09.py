from dataclasses import dataclass

numeroLinhas: int = int(input())
numeroColunas: int = 0
matrizComodo: list[str] = []

for _ in range(numeroLinhas):
    linha: list[str] = input().split(' ')
    numeroColunas = len(linha)
    for i in range(len(linha)):
        matrizComodo.append(linha[i])


@dataclass
class Robo:
    matrizComodo: list[str]
    numeroColunas: int
    numeroLinhas: int
    indiceRobo: int = 0
    posicoesNaoPassadas: int = len(matrizComodo) - 1
    tarefaEmExecusao: bool = True
    modoAtual: str = 'escanearAmbiente'
    ultimaPosicaoEscaneada: int = 0
    posicaoDaSujeira: int = 0
    proximaPosicao: int = 0

    def limparComodo(self) -> None:
        self._mostraComodo('primeiraVez')
        while self.tarefaEmExecusao:
            match self.modoAtual:
                case 'escanearAmbiente':
                    self._escaneamentoAmbiente()
                case 'limparAmbiente':
                    self._limpandoAmbiente()
                case 'retornarEscaneamentoAmbiente':
                    self._retornarEscaneamentoAmbiente()
                case 'finalizarLimpeza':
                    self._finalizarLimpeza()

    def _escaneamentoAmbiente(self) -> None:
        self._direcaoMovimento()
        self._encontraSujeira()
        if self.posicoesNaoPassadas == 0:
            self.modoAtual = 'finalizarLimpeza'
        elif self.posicaoDaSujeira == 0:
            self._andar(self.proximaPosicao)
            self.posicoesNaoPassadas -= 1
            self._mostraComodo()
        else:
            self.ultimaPosicaoEscaneada = self.indiceRobo
            self.modoAtual = 'limparAmbiente'

    def _limpandoAmbiente(self) -> None:
        self._encontraSujeira()
        if self.proximaPosicao == self.indiceRobo:
            self.posicoesNaoPassadas -= 1
            self.ultimaPosicaoEscaneada = self.indiceRobo
            self.modoAtual = 'escanearAmbiente'
        elif self.posicaoDaSujeira != 0:
            self._andar(self.posicaoDaSujeira)
            self._mostraComodo()
        else:
            self.modoAtual = 'retornarEscaneamentoAmbiente'

    def _retornarEscaneamentoAmbiente(self) -> None:
        indiceIJAnterior: tuple[int, int] = self._indiceIJ(self.ultimaPosicaoEscaneada)
        indiceIJAtual: tuple[int, int] = self._indiceIJ(self.indiceRobo)
        deslocamentoColuna: int = indiceIJAtual[1] - indiceIJAnterior[1]
        sujeiraEncontrada: bool = False
        for coluna in range(deslocamentoColuna if deslocamentoColuna > 0 else - deslocamentoColuna):
            self._encontraSujeira()
            if self.posicaoDaSujeira != 0:
                sujeiraEncontrada = True
                break
            elif deslocamentoColuna > 0:
                self._andar(self.indiceRobo - 1)
            else:
                self._andar(self.indiceRobo + 1)
            self._mostraComodo()
        for linha in range(indiceIJAtual[0] - indiceIJAnterior[0]):
            self._encontraSujeira()
            if self.posicaoDaSujeira != 0:
                sujeiraEncontrada = True
                break
            self._andar(self.indiceRobo - self.numeroColunas)
            self._mostraComodo()
        if sujeiraEncontrada:
            self.modoAtual = 'limparAmbiente'
        else:
            self.modoAtual = 'escanearAmbiente'

    def _finalizarLimpeza(self) -> None:
        indicesIJ: tuple[int, int] = self._indiceIJ(self.indiceRobo)
        if indicesIJ[1] == self.numeroColunas - 1:
            self.tarefaEmExecusao = False
        else:
            for _ in range(len(self.matrizComodo) - self.indiceRobo - 1):
                self._andar(self.indiceRobo + 1)
                self._mostraComodo()
            self.tarefaEmExecusao = False

    def _mostraComodo(self, primeiraVez: str = '') -> None:
        if primeiraVez != 'primeiraVez':
            print()
        for i in range(self.numeroLinhas):
            for j in range(self.numeroColunas):
                if j == self.numeroColunas - 1:
                    print(self.matrizComodo[i * numeroColunas + j], end="\n")
                else:
                    print(self.matrizComodo[i * numeroColunas + j], end=" ")

    def _encontraSujeira(self) -> None:
        IJRobo: tuple[int, int] = self._indiceIJ(self.indiceRobo)
        if IJRobo[1] != 0 and self.matrizComodo[self.indiceRobo - 1] == 'o':
            self.posicaoDaSujeira = self.indiceRobo - 1
        elif IJRobo[0] != 0 and self.matrizComodo[self.indiceRobo - self.numeroColunas] == 'o':
            self.posicaoDaSujeira = self.indiceRobo - self.numeroColunas
        elif IJRobo[1] != self.numeroColunas - 1 and self.matrizComodo[self.indiceRobo + 1] == 'o':
            self.posicaoDaSujeira = self.indiceRobo + 1
        elif IJRobo[0] != self.numeroLinhas - 1 and self.matrizComodo[self.indiceRobo + self.numeroColunas] == 'o':
            self.posicaoDaSujeira = self.indiceRobo + self.numeroColunas
        else:
            self.posicaoDaSujeira = 0

    def _andar(self, posicao: int) -> None:
        self.matrizComodo[self.indiceRobo] = '.'
        self.matrizComodo[posicao] = 'r'
        self.indiceRobo = posicao

    def _direcaoMovimento(self) -> None:
        indicesIJ: tuple[int, int] = self._indiceIJ(self.indiceRobo)
        if indicesIJ[0] % 2 == 0 and indicesIJ[1] != self.numeroColunas - 1:
            self.proximaPosicao = self.indiceRobo + 1
        elif indicesIJ[0] % 2 != 0 and indicesIJ[1] != 0:
            self.proximaPosicao = self.indiceRobo - 1
        else:
            self.proximaPosicao = self.indiceRobo + numeroColunas

    def _indiceIJ(self, indiceK: int) -> tuple[int, int]:
        i: int = indiceK // self.numeroColunas
        j: int = indiceK % self.numeroColunas
        return i, j


robo = Robo(matrizComodo, numeroColunas, numeroLinhas)
robo.limparComodo()
