# Preenche um dicionário com a chave sendo o tipo da flecha e o valor a quantidade disponível da mesma
from math import floor
from xml.etree.ElementInclude import include

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

# Calcula o dano do ataque de Aloy
def calculaDanoAtaque(infoMonstros, infoAtaque):
    infoParteAlvo: list = infoMonstros[infoAtaque['unidadeAlvo']]['partes'][infoAtaque['parteAlvo']]
    cordenadaCritica: tuple = infoParteAlvo[2]
    cordenadaFlecha: tuple = infoAtaque['cordenadasFlecha']
    danoMaximo: int = infoParteAlvo[1]
    distanciaX: int = cordenadaCritica[0] - cordenadaFlecha[0]
    moduloDistanciaX: int = distanciaX if distanciaX > 0 else - distanciaX
    distanciaY: int = cordenadaCritica[1] - cordenadaFlecha[1]
    moduloDistanciaY: int = distanciaY if distanciaY > 0 else - distanciaY
    if danoMaximo - (moduloDistanciaX + moduloDistanciaY) > 0:
        danoTotal: int = danoMaximo - (moduloDistanciaX + moduloDistanciaY)
    else:
        danoTotal: int = 0
    criticosAcertados = None
    if moduloDistanciaX == 0 and moduloDistanciaY == 0:
        criticosAcertados = cordenadaCritica

    if infoParteAlvo[0] == infoAtaque['flechaUsada'] or infoParteAlvo[0] == 'todas':
        return [danoTotal, criticosAcertados]
    else:
        return [danoTotal // 2, criticosAcertados]
    
def imprimeRelatorioCombate(relatorioCombate, flechasDisponiveis = {}):
    indiceCombate = relatorioCombate['indiceCombate']
    vidaAloy = relatorioCombate['pontosVidaAloy']
    vidaAloyAposCombate = relatorioCombate['vidaAloyAposCombate']
    flechasUtilizadas = relatorioCombate['flechasUtilizadas']
    print(f'Combate {indiceCombate}, vida = {vidaAloy}')
    maquinasDerrotadas = relatorioCombate['maquinasDerrotadas']
    for indiceMaquina in maquinasDerrotadas:
        print(f'Máquina {indiceMaquina} derrotada')
    print(f'Vida após o combate = {vidaAloyAposCombate}')
    dicionarioFlechas = {}
    for tipo in flechasDisponiveis.keys():
        for flecha in flechasUtilizadas:
            if tipo == flecha:
                dicionarioFlechas[flecha] = flechasUtilizadas.count(flecha)
    print('Flechas utilizadas:')
    for chave,valor in dicionarioFlechas.items():
        flechasTotais = flechasDisponiveis[chave]
        print(f'- {chave}: {valor}/{flechasTotais}')

    criticos = relatorioCombate['criticosAcertados']
    if criticos:
        monstros = relatorioCombate['monstros']
        print('Críticos acertados:')
        dicionarioCritico = {}
        maquinas = []
        for i in range(len(monstros)):
            dicionarioCritico[i] = {}
            for j in monstros[i]['partes'].values():
                dicionarioCritico[i][j[2]] = 0 
                for critico in criticos:
                    if j[2] == critico[1] and i in critico:
                        dicionarioCritico[i][j[2]] += 1
                        if maquinas.count(critico[0]) == 0:
                            maquinas.append(critico[0])

        for i in maquinas:
            for chave,valor in dicionarioCritico.items():
                if chave == i:
                    print(f'Máquina {chave}:')
                    for chave,valor in valor.items():
                        if valor != 0:
                            print(f'- {chave}: {valor}x')


def combate(pontosVidaAloy, flechasDisponiveis, quantidadeMonstrosTotal):
    monstrosRestantes: int = quantidadeMonstrosTotal
    pontosVidaAloyTotal: int = pontosVidaAloy
    relatorioCombate: dict = {}
    indiceCombate: int = 0
    acabouFlechas = False
    while monstrosRestantes != 0 and acabouFlechas == False and pontosVidaAloy > 0:
        flechasTotais = flechasDisponiveis.copy()
        totalFlechas = 0
        for valor in flechasTotais.values():
            totalFlechas += int(valor)
        relatorioCombate['indiceCombate'] = indiceCombate
        relatorioCombate['pontosVidaAloy'] = pontosVidaAloy
        relatorioCombate['flechasUtilizadas'] = []
        relatorioCombate['maquinasDerrotadas'] = []
        relatorioCombate['criticosAcertados'] = []
        quantidadeMonstrosCombate: int = int(input())
        quantidadeMonstrosCombateInicial = quantidadeMonstrosCombate
        listaMonstros: list[dict] = preencheListaMonstros(quantidadeMonstrosCombate)
        relatorioCombate['monstros'] = listaMonstros
        # Rodada do combate
        monstrosVivos: int = quantidadeMonstrosCombate
        while monstrosVivos != 0 and pontosVidaAloy > 0 and acabouFlechas == False:
            relatorioCombate['vidaAloyAposCombate'] = pontosVidaAloy
            # Ataque Aloy
            for _ in range(3):
                informacoesAtaque: dict = preencheInformacoesAtaque(input().split(', '))
                relatorioCombate['flechasUtilizadas'].append(informacoesAtaque['flechaUsada'])
                quantidadeDisponivel = int(flechasTotais[informacoesAtaque['flechaUsada']])
                quantidadeDisponivel -= 1
                totalFlechas -= 1
                if quantidadeDisponivel < 0 or totalFlechas == 0:
                    acabouFlechas = True
                    break
                flechasTotais[informacoesAtaque['flechaUsada']] = quantidadeDisponivel
                unidadeAlvo: int = informacoesAtaque['unidadeAlvo']
                infosAtaque = calculaDanoAtaque(listaMonstros, informacoesAtaque)
                if infosAtaque[1] != None:
                    relatorioCombate['criticosAcertados'].append([unidadeAlvo, infosAtaque[1]])
                vidaMonstro = listaMonstros[unidadeAlvo]['pontosVida']
                vidaMonstro -= infosAtaque[0]
                listaMonstros[unidadeAlvo]['pontosVida'] = vidaMonstro
                if vidaMonstro <= 0:
                    monstrosVivos -= 1
                    relatorioCombate['maquinasDerrotadas'].append(unidadeAlvo)
                    if monstrosVivos == 0:
                        break
            # Ataque monstro
            if monstrosVivos != 0:
                for indiceMonstro in range(quantidadeMonstrosCombateInicial):
                    if indiceMonstro not in relatorioCombate['maquinasDerrotadas']:
                        pontosVidaAloy -= listaMonstros[indiceMonstro]['pontosAtaque']
                        relatorioCombate['vidaAloyAposCombate'] = pontosVidaAloy
        if pontosVidaAloy > 0 and acabouFlechas == False:
            imprimeRelatorioCombate(relatorioCombate, flechasDisponiveis)
            pontosVidaAloy += floor(0.5 * pontosVidaAloyTotal)
            if pontosVidaAloy > pontosVidaAloyTotal:
                excedente = pontosVidaAloy - pontosVidaAloyTotal
                pontosVidaAloy -= excedente
        else:
            print(f'Combate {indiceCombate}, vida = {pontosVidaAloyTotal}')
            if pontosVidaAloy < 0:
                pontosVidaAloy -= pontosVidaAloy
            maquinasDerrotadas = relatorioCombate['maquinasDerrotadas']
            for indiceMaquina in maquinasDerrotadas:
                print(f'Máquina {indiceMaquina} derrotada')
            print(f'Vida após o combate = {pontosVidaAloy}')
        monstrosRestantes = monstrosRestantes - quantidadeMonstrosCombateInicial
        indiceCombate += 1
    if pontosVidaAloy > 0 and acabouFlechas == False:
        print('Aloy provou seu valor e voltou para sua tribo.')
    elif acabouFlechas == True:
        print('Aloy ficou sem flechas e recomeçará sua missão mais preparada.')
    else:
        print('Aloy foi derrotada em combate e não retornará a tribo.')

def main() -> None:
    pontosVidaAloy: int = int(input())
    flechasDisponiveis: dict[str, int] = preencheFlechasDisponiveis(input().split(' '))
    quantidadeMonstrosTotal: int = int(input())
    combate(pontosVidaAloy, flechasDisponiveis, quantidadeMonstrosTotal)


if __name__ == '__main__':
    main()
