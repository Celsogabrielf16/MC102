from dataclasses import dataclass
from math import floor


# Preenche um dicionário com a chave sendo o tipo da flecha e o valor a quantidade disponível da mesma
def preencheFlechasDisponiveis(lista: list) -> dict:
    dictFlechas: dict = {}
    for indice in range(0, len(lista), 2):
        dictFlechas[lista[indice]] = lista[indice + 1]
    return dictFlechas


# Não sei se é a utilização 100% correta da classe, mas foi a maneira mais organizada que encontrei para resolver o lab :)
@dataclass
class Combate:
    vidaAloy: int
    flechasDisponiveis: dict
    quantidadeMaquinas: int
    relatorioCombate: dict
    maquinasRestantes: int = 0
    vidaAloyTotal: int = 0
    indiceCombate: int = 0
    quantidadeMaquinasCombate: int = 0
    maquinasRestantesCombate: int = 0
    flechasTotaisCombate: int = 0
    acabouFlechas: bool = False

    # Da inicio aos combates
    def comecaCombate(self) -> None:
        self.maquinasRestantes = self.quantidadeMaquinas
        self.vidaAloyTotal = self.vidaAloy
        while self.maquinasRestantes != 0 and self.acabouFlechas is False and self.vidaAloy > 0:
            self._combate()
            self.maquinasRestantes -= self.quantidadeMaquinasCombate
            self.indiceCombate += 1
        self._imprimeDesfecho()

    # Combate entre a Aloy e as U máquinas
    def _combate(self) -> None:
        flechasDisponiveisCombate: dict = self._calculaTotalFlechas()
        self._criaRelatorioCombate()
        self.quantidadeMaquinasCombate = int(input())
        listaInfoMaquinas: list = self._preencheInformacoesMaquinas(self.quantidadeMaquinasCombate)
        self.relatorioCombate['maquinas'] = listaInfoMaquinas

        self.maquinasRestantesCombate = self.quantidadeMaquinasCombate
        while self.maquinasRestantesCombate != 0 and self.vidaAloy > 0 and self.acabouFlechas is False:
            self.relatorioCombate['vidaAloyAposCombate'] = self.vidaAloy
            self._ataqueAloy(flechasDisponiveisCombate, listaInfoMaquinas)
            self._ataqueMaquinas(listaInfoMaquinas)
        self._imprimeDesfechoCombate()

    # Calcula quantas flechas estão disponiveis no total, e retorna uma copia do dicionario principal, para podemos ter
    # controle de quantas flechas de cada tipo ainda estão disponiveis após cada ataque, sem modificar o dicionario principal
    def _calculaTotalFlechas(self) -> dict:
        self.flechasTotaisCombate = 0
        flechasDisponiveisCombate: dict = self.flechasDisponiveis.copy()
        for valor in flechasDisponiveisCombate.values():
            self.flechasTotaisCombate += int(valor)
        return flechasDisponiveisCombate

    # Cria um dicionario onde será armazenado todas as informações que vão ser imprimidas posteriormente
    def _criaRelatorioCombate(self) -> None:
        self.relatorioCombate['indiceCombate'] = self.indiceCombate
        self.relatorioCombate['vidaAloy'] = self.vidaAloy
        self.relatorioCombate['flechasUtilizadas'] = []
        self.relatorioCombate['maquinasDerrotadas'] = []
        self.relatorioCombate['criticosAcertados'] = []

    # Preenche uma lista com as informações das maquinas dispostas em um dicionário
    def _preencheInformacoesMaquinas(self, quantidadeMaquinas: int) -> list:
        listaMaquinas: list = []
        # Laço para preencher um dicionario com informações das maquinas
        for _ in range(quantidadeMaquinas):
            infoMaquinas: list[int] = [int(info) for info in input().split(' ')]
            dictInfoMaquinas: dict = {}
            dictInfoMaquinas['pontosVida'] = infoMaquinas[0]
            dictInfoMaquinas['pontosAtaque'] = infoMaquinas[1]
            dictInfoMaquinas['quantidadePartes'] = infoMaquinas[2]
            dictInfoMaquinas['partes'] = {}
            # Laço para preencher um dicionario com informações das partes da maquina
            for _ in range(infoMaquinas[2]):
                partes: list = input().split(', ')
                dictInfoPartes: list = [partes[1], int(partes[2]), (int(partes[3]), int(partes[4]))]
                dictInfoMaquinas['partes'][partes[0]] = dictInfoPartes
            listaMaquinas.append(dictInfoMaquinas)
        return listaMaquinas

    # Efetua o ataque da Aloy as U maquinas
    def _ataqueAloy(self, flechasDisponiveisCombate: dict, infoMaquinas: list) -> None:
        # Como Aloy pode atirar três vezes seguidas precisamos de um loop
        for _ in range(3):
            infoAtaque: dict = self._preencheInformacoesAtaque(input().split(', '))

            # Aqui calculamos quantas flechas ainda estão disponiveis, e se ainda tiver
            # flechas atualizamos pois ela utilizou a determinada flecha no combate
            self.relatorioCombate['flechasUtilizadas'].append(infoAtaque['flechaUsada'])
            quantidadeDisponivel: int = int(flechasDisponiveisCombate[infoAtaque['flechaUsada']])
            quantidadeDisponivel -= 1
            self.flechasTotaisCombate -= 1
            # Se acabou as flechas de determinado tipo, ou todas as flechas, não precisamos continuar
            if quantidadeDisponivel < 0 or self.flechasTotaisCombate == 0:
                self.acabouFlechas = True
                break
            flechasDisponiveisCombate[infoAtaque['flechaUsada']] = quantidadeDisponivel

            # Aqui calculamos o dano dado por Aloy, e se acertou o ponto critico
            unidadeAlvo: int = infoAtaque['unidadeAlvo']
            danoTotal, criticosAcertados = self._calculaDanoECriticoAtaque(infoMaquinas, infoAtaque)
            if criticosAcertados is not None:
                self.relatorioCombate['criticosAcertados'].append([unidadeAlvo, criticosAcertados])

            # Aqui descontamos o dano calculado na maquina alvo do ataque
            vidaMaquinas: int = infoMaquinas[unidadeAlvo]['pontosVida']
            vidaMaquinas -= danoTotal
            infoMaquinas[unidadeAlvo]['pontosVida'] = vidaMaquinas
            if vidaMaquinas <= 0:
                self.maquinasRestantesCombate -= 1
                self.relatorioCombate['maquinasDerrotadas'].append(unidadeAlvo)
                if self.maquinasRestantesCombate == 0:
                    break

    # Preenche um dicionário com as informações do ataque da Aloy
    def _preencheInformacoesAtaque(self, infoAtaque: list) -> dict:
        dictInfoAtaque: dict = {}
        dictInfoAtaque['unidadeAlvo'] = int(infoAtaque[0])
        dictInfoAtaque['parteAlvo'] = infoAtaque[1]
        dictInfoAtaque['flechaUsada'] = infoAtaque[2]
        dictInfoAtaque['cordenadasFlecha'] = (int(infoAtaque[3]), int(infoAtaque[4]))
        return dictInfoAtaque

    # Calcula o dano do ataque de Aloy
    def _calculaDanoECriticoAtaque(self, infoMaquinas: list, infoAtaque: dict) -> list:
        infoParteAlvo: list = infoMaquinas[infoAtaque['unidadeAlvo']]['partes'][infoAtaque['parteAlvo']]
        cordenadaCritica: tuple = infoParteAlvo[2]
        cordenadaFlecha: tuple = infoAtaque['cordenadasFlecha']

        distanciaFlechaPontoCritico: list = self._calculaDistanciaPontoCritico(cordenadaCritica, cordenadaFlecha)
        danoTotal: int = self._calculaDanoTotal(infoParteAlvo[1], distanciaFlechaPontoCritico)
        criticosAcertados: tuple = distanciaFlechaPontoCritico[2]

        # Verefica se a flecha usada por Aloy é do tipo da fraqueza da parte alvo
        if infoParteAlvo[0] == infoAtaque['flechaUsada'] or infoParteAlvo[0] == 'todas':
            return [danoTotal, criticosAcertados]
        else:
            return [danoTotal // 2, criticosAcertados]

    # Calcula a distancia entre o ponto acertado por aloy e o ponto critico da parte alvo, retornando a
    # distancia X e Y, e caso as duas forem zero significa que ela acertou exatamente o ponto critico
    def _calculaDistanciaPontoCritico(self, cordenadaCritica: tuple, cordenadaFlecha: tuple) -> list:
        distanciaX: int = cordenadaCritica[0] - cordenadaFlecha[0]
        moduloDistanciaX: int = distanciaX if distanciaX > 0 else - distanciaX

        distanciaY: int = cordenadaCritica[1] - cordenadaFlecha[1]
        moduloDistanciaY: int = distanciaY if distanciaY > 0 else - distanciaY

        # Verifica se Aloy acertou o ponto critico
        if moduloDistanciaX == 0 and moduloDistanciaY == 0:
            return [moduloDistanciaX, moduloDistanciaY, cordenadaCritica]
        else:
            return [moduloDistanciaX, moduloDistanciaY, None]

    # Calcula o dano total que Aloy pode dar
    def _calculaDanoTotal(self, danoMaximo: int, distanciaFlechaPontoCritico: list) -> int:
        if danoMaximo - (distanciaFlechaPontoCritico[0] + distanciaFlechaPontoCritico[1]) > 0:
            return danoMaximo - (distanciaFlechaPontoCritico[0] + distanciaFlechaPontoCritico[1])
        else:
            return 0

    # Desconta o dano de ataque das U maquinas restantes na vida de Aloy
    def _ataqueMaquinas(self, listaInfoMaquinas: list) -> None:
        if self.maquinasRestantesCombate != 0:
            for indiceMaquina in range(self.quantidadeMaquinasCombate):
                if indiceMaquina not in self.relatorioCombate['maquinasDerrotadas']:
                    self.vidaAloy -= listaInfoMaquinas[indiceMaquina]['pontosAtaque']
                    self.relatorioCombate['vidaAloyAposCombate'] = self.vidaAloy

    # Imprime as informações do combate
    def _imprimeDesfechoCombate(self) -> None:
        if self.vidaAloy > 0 and self.acabouFlechas is False:
            self._imprimeRelatorioCombate()
            self.vidaAloy += floor(0.5 * self.vidaAloyTotal)
            if self.vidaAloy > self.vidaAloyTotal:
                excedente: int = self.vidaAloy - self.vidaAloyTotal
                self.vidaAloy -= excedente
        else:
            print(f'Combate {self.indiceCombate}, vida = {self.vidaAloyTotal}')
            if self.vidaAloy < 0:
                self.vidaAloy -= self.vidaAloy
            maquinasDerrotadas: list = self.relatorioCombate['maquinasDerrotadas']
            for indiceMaquina in maquinasDerrotadas:
                print(f'Máquina {indiceMaquina} derrotada')
            print(f'Vida após o combate = {self.vidaAloy}')

    # Imprime o relatorio completo do combate de Aloy e as maquinas
    def _imprimeRelatorioCombate(self) -> None:
        self._imprimeIndiceCombateEVida(self.relatorioCombate['indiceCombate'], self.relatorioCombate['vidaAloy'])
        self._imprimeMaquinasDerrotadas(self.relatorioCombate['maquinasDerrotadas'])
        self._imprimeVidaAposCombate(self.relatorioCombate['vidaAloyAposCombate'])
        self._imprimeFlechasUtilizadas(self.relatorioCombate['flechasUtilizadas'])
        self._imprimeCriticoAcertados()

    def _imprimeIndiceCombateEVida(self, indiceCombate: int, vidaAloy: int) -> None:
        print(f'Combate {indiceCombate}, vida = {vidaAloy}')

    def _imprimeMaquinasDerrotadas(self, maquinasDerrotadas: list) -> None:
        for indiceMaquina in maquinasDerrotadas:
            print(f'Máquina {indiceMaquina} derrotada')

    def _imprimeVidaAposCombate(self, vidaAloyAposCombate: int) -> None:
        print(f'Vida após o combate = {vidaAloyAposCombate}')

    def _imprimeFlechasUtilizadas(self, flechasUtilizadas: list) -> None:
        dicionarioFlechas: dict = {}
        for tipoFlecha in self.flechasDisponiveis.keys():
            for flecha in flechasUtilizadas:
                if tipoFlecha == flecha:
                    dicionarioFlechas[flecha] = flechasUtilizadas.count(flecha)
        print('Flechas utilizadas:')
        for chave, valor in dicionarioFlechas.items():
            flechasTotais: int = self.flechasDisponiveis[chave]
            print(f'- {chave}: {valor}/{flechasTotais}')

    def _imprimeCriticoAcertados(self) -> None:
        listaCriticosAcertados = self.relatorioCombate['criticosAcertados']
        if listaCriticosAcertados:
            maquinas = self.relatorioCombate['maquinas']
            print('Críticos acertados:')
            dicionarioCritico: dict = {}
            maquinasAcertadas: list = []
            for i in range(len(maquinas)):
                dicionarioCritico[i] = {}
                for j in maquinas[i]['partes'].values():
                    dicionarioCritico[i][j[2]] = 0
                    for criticoAcertado in listaCriticosAcertados:
                        if j[2] == criticoAcertado[1] and i in criticoAcertado:
                            dicionarioCritico[i][j[2]] += 1
                            if maquinasAcertadas.count(criticoAcertado[0]) == 0:
                                maquinasAcertadas.append(criticoAcertado[0])
            for i in maquinasAcertadas:
                for chave, valor in dicionarioCritico.items():
                    if chave == i:
                        print(f'Máquina {chave}:')
                        for chave, valor in valor.items():
                            if valor != 0:
                                print(f'- {chave}: {valor}x')

    # Imprime o desfecho final de Aloy
    def _imprimeDesfecho(self) -> None:
        if self.vidaAloy > 0 and self.acabouFlechas is False:
            print('Aloy provou seu valor e voltou para sua tribo.')
        elif self.acabouFlechas is True:
            print('Aloy ficou sem flechas e recomeçará sua missão mais preparada.')
        else:
            print('Aloy foi derrotada em combate e não retornará a tribo.')


def main() -> None:
    vidaAloy: int = int(input())
    flechasDisponiveis: dict[str, int] = preencheFlechasDisponiveis(input().split(' '))
    quantidadeMaquinas: int = int(input())
    combate = Combate(vidaAloy, flechasDisponiveis, quantidadeMaquinas, dict())
    combate.comecaCombate()


if __name__ == '__main__':
    main()
