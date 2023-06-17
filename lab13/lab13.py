from dataclasses import dataclass
import sys
sys.setrecursionlimit(161004)


@dataclass
class Ferramenta:
    caminhoImagem: str
    listaOperacoes: list[list]
    matrizImagem: list[list[int]]
    numeroColunasMatriz: int = 0
    numeroLinhasMatriz: int = 0
    intensidadeMaxima: int = 0
    corBucket: int = 256

    # Inicicia a ferramenta lendo o arquivo, e executando cada operação dada uma por vez
    def iniciaFerramenta(self) -> None:
        self._leituraArquivo()

        for operacao in self.listaOperacoes:
            self._executarOperacao(operacao)

    # Verifica qual a operação desejada e redereciona para o método correto
    def _executarOperacao(self, operacao: list) -> None:
        match operacao[0]:
            case 'bucket':
                self._bucket(operacao[1], operacao[2], operacao[3], operacao[4])
            case 'negative':
                self._negative(operacao[1], operacao[2], operacao[3])
            case 'cmask':
                self._cmask(operacao[1], operacao[2], operacao[3])
            case 'save':
                self._save(operacao[1])

    # Operação save, salva o arquivo pgm com a imagem apos as operações
    def _save(self, caminho: str) -> None:
        with open(caminho, 'w') as arquivo:
            arquivo.write('P2\n')
            arquivo.write('# Imagem criada pelo lab13\n')
            arquivo.write(f'{self.numeroColunasMatriz} {self.numeroLinhasMatriz}\n')
            arquivo.write(f'{self.intensidadeMaxima}\n')
            for linha in self.matrizImagem:
                indiceCor: int = 0
                for cor in linha:
                    indiceCor += 1
                    if indiceCor == 1:
                        arquivo.write(f'{cor}')
                    else:
                        arquivo.write(f' {cor}')
                arquivo.write('\n')

    # Operação bucket, pinta a regiao conexa com a cor dada
    def _bucket(self, cor: int, tolerancia: int, coluna: int, linha: int) -> None:
        self.corBucket = cor
        regiaoConexa: list[list[int]] = self._buscaRegioesConexas(tolerancia, coluna, linha)
        self.matrizImagem = self._trocaCorMatriz(cor, regiaoConexa, self.matrizImagem)

    # Operação negative, troca a cor da regiao conexa com o inverso da mesma
    def _negative(self, tolerancia: int, coluna: int, linha: int) -> None:
        regiaoConexa: list[list[int]] = self._buscaRegioesConexas(tolerancia, coluna, linha)
        self._trocaCorMatrizPorCorNegativa(regiaoConexa)

    # Operação cmask, retorna uma matriz de 0 e 255, sendo ela a mascara da regiao conexa do ponto selecionado
    def _cmask(self, tolerancia: int, coluna: int, linha: int) -> None:
        regiaoConexa: list[list[int]] = self._buscaRegioesConexas(tolerancia, coluna, linha)
        matrizMascara: list = self._criaListaComONumero(255)
        self.matrizImagem = self._trocaCorMatriz(0, regiaoConexa, matrizMascara)

    # Troca as cores da matrizImagem de acordo com a matriz mascara, pela cor negativa
    def _trocaCorMatrizPorCorNegativa(self, mascara: list) -> None:
        for indiceLinha in range(len(self.matrizImagem)):
            for indiceColuna in range(len(self.matrizImagem[indiceLinha])):
                if mascara[indiceLinha][indiceColuna] == 1:
                    cor: int = self.intensidadeMaxima - self.matrizImagem[indiceLinha][indiceColuna]
                    self.matrizImagem[indiceLinha][indiceColuna] = cor

    # Troca as cores da matrizImagem de acordo com a matriz mascara, pela cor desejada
    def _trocaCorMatriz(self, cor: int, mascara: list, matriz: list) -> list:
        for indiceLinha in range(len(matriz)):
            for indiceColuna in range(len(matriz[indiceLinha])):
                if mascara[indiceLinha][indiceColuna] == 1:
                    matriz[indiceLinha][indiceColuna] = cor
        return matriz

    # Retorna uma matriz de 0 e 1, sendo o 1 os ponstos conexos ao ponto dado na operacao
    def _buscaRegioesConexas(self, tolerancia: int, coluna: int, linha: int) -> list[list[int]]:
        regiaoConexa: list[list[int]] = self._criaListaComONumero(0)
        cor: int = self.matrizImagem[linha][coluna]
        listaRegiao = self._buscaRegioesConexasRec(cor, cor, tolerancia, coluna, linha, regiaoConexa)
        return listaRegiao

    def _buscaRegioesConexasRec(self, intencidadeCor, intencidadeCorAtual, tolerancia, coluna, linha, listaRegiaoConexa) -> list:
        intencidadeCorAtual: int = self.matrizImagem[linha][coluna]
        if abs(intencidadeCorAtual - intencidadeCor) <= tolerancia and listaRegiaoConexa[linha][coluna] != 1:
            listaRegiaoConexa[linha][coluna] = 1
            possiveisPosicoesConexas = self._encontraPossiveisPosicoesConexas(coluna, linha)
            for posicao in possiveisPosicoesConexas:
                colunaAtual = posicao[1]
                linhaAtual = posicao[0]
                intencidadeCorAtual: int = self.matrizImagem[linhaAtual][colunaAtual]
                listaRegiaoConexa = self._buscaRegioesConexasRec(intencidadeCor, intencidadeCorAtual, tolerancia, colunaAtual, linhaAtual, listaRegiaoConexa)
            return listaRegiaoConexa
        return listaRegiaoConexa
    
    def _encontraPossiveisPosicoesConexas(self, coluna: int, linha: int) -> list[tuple[int, int]]:
        listaPosicoes: list = []
        tupla: tuple[int, int] = (0, 0)
        if linha != self.numeroLinhasMatriz - 1:
            tupla = linha + 1, coluna
            listaPosicoes.append(tupla)
            if coluna != self.numeroColunasMatriz - 1:
                tupla = linha + 1, coluna + 1
                listaPosicoes.append(tupla)
            if coluna != 0:
                tupla = linha + 1, coluna - 1
                listaPosicoes.append(tupla)
        if linha != 0:
            tupla = linha - 1, coluna
            listaPosicoes.append(tupla)
            if coluna != self.numeroColunasMatriz - 1:
                tupla = linha - 1, coluna + 1
                listaPosicoes.append(tupla)
            if coluna != 0:
                tupla = linha - 1, coluna - 1
                listaPosicoes.append(tupla)
        if coluna != 0:
            tupla = linha, coluna - 1
            listaPosicoes.append(tupla)
        if coluna != self.numeroColunasMatriz - 1:
            tupla = linha, coluna + 1
            listaPosicoes.append(tupla)
        return listaPosicoes

    # Cria uma matriz do tamanho da matrizImagem, preenchida com o numero determinado
    def _criaListaComONumero(self, numero: int) -> list[list[int]]:
        listaFinal: list = []
        for _ in range(self.numeroLinhasMatriz):
            listaLinha: list = []
            for _ in range(self.numeroColunasMatriz):
                listaLinha.append(numero)
            listaFinal.append(listaLinha)
        return listaFinal

    # Le o arquivo dado, e guarda as informações uteis
    def _leituraArquivo(self) -> None:
        import os
        print(os.getcwd())
        arquivo = open(self.caminhoImagem)

        linhasArquivo: list = arquivo.readlines()

        tamanhoMatriz = self._limpaLista(linhasArquivo[2].split(' '))
        self.numeroColunasMatriz = tamanhoMatriz[0]
        self.numeroLinhasMatriz = tamanhoMatriz[1]

        self.intensidadeMaxima = int(linhasArquivo[3])

        for indiceLinha in range(4, len(linhasArquivo), 1):
            linhaLimpa: list = self._limpaLista(linhasArquivo[indiceLinha].split(' '))
            self.matrizImagem.append(linhaLimpa)

        arquivo.close()

    # No arquivo dado existem espaços não uniformes entre as colunas da matriz, essa função limpa esses espaços
    # retornando uma lista apenas com os elementos
    def _limpaLista(self, lista: list) -> list:
        listaCaracteres: list = []
        for caracteres in lista:
            caracter: list = []
            for numero in caracteres:
                if numero in '0123456789' and len(numero) != 0:
                    caracter.append(numero)
            listaCaracteres.append(caracter)

        listaFinal: list = []
        for elemento in listaCaracteres:
            if len(elemento) != 0:
                listaFinal.append(''.join(elemento))
        return self._converteParaInteiro(listaFinal)

    # Converte a lista de strings dadas para uma lista de inteiros
    def _converteParaInteiro(self, lista: list[str]) -> list[int]:
        listaFinal: list = []
        for caracter in lista:
            listaFinal.append(int(caracter))
        return listaFinal


def main() -> None:
    caminhoImagem: str = input()
    numeroOperacoes: int = int(input())
    listaOperacoes: list[list] = preencheListaOperacoes(numeroOperacoes)

    ferramenta = Ferramenta(caminhoImagem, listaOperacoes, list())
    ferramenta.iniciaFerramenta()


def preencheListaOperacoes(numeroOperacoes: int) -> list[list]:
    listaFinal: list = []
    for _ in range(numeroOperacoes):
        listaOperacao: list = []
        operacao: list = input().split(' ')
        if operacao[0] != 'save':
            listaOperacao.append(operacao[0])
            for indiceNumero in range(1, len(operacao), 1):
                listaOperacao.append(int(operacao[indiceNumero]))
            listaFinal.append(listaOperacao)
        else:
            listaFinal.append(operacao)
    return listaFinal


if __name__ == '__main__':
    main()
