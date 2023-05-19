genoma: str = input()

def separaString(string: str, i: int, j: int) -> list():
    stringList = list(string)
    listaAntecede: list = [] # elemantos antecessores a i, se existirem
    listaPrincipal: list = [] # elementos do conjunto [i, j]
    listaSucede: list = [] # elementos sucessores a j, se existirem
    indiceLista: int = 0 # Guarda o indice de cada caracter na lista
    for caracter in stringList:
        if indiceLista >= int(i) and indiceLista <= int(j):
            listaPrincipal.append(caracter)
        elif indiceLista < int(i) and int(i) > 0:
            listaAntecede.append(caracter)
        elif indiceLista > int(j) and int(j) < len(string):
            listaSucede.append(caracter)
        indiceLista += 1
    return [''.join(listaAntecede), ''.join(listaPrincipal), ''.join(listaSucede)]

def verificaIndices(i: int, j: int = 0, regra: int = 0):
    if i > len(genoma) and regra == 3:
        return False
    elif (i > len(genoma) or j > len(genoma)) and regra == 4:
        return False
    return True

def reverter(i: int, j: int, g: str) -> str:
    genomaSeparado: list = separaString(g, i, j)
    return ''.join([genomaSeparado[0], genomaSeparado[1][::-1], genomaSeparado[2]])

def transpor(i: int, j: int, k: int) -> str:
    listaIJ: list = separaString(genoma, i, j)
    listaJK: list = separaString(genoma, j + 1, k)
    return ''.join([listaIJ[0], listaJK[1], listaIJ[1], listaJK[2]])

def combinar(g: str, i: int) -> str:
    genomaSeparado: list = list(genoma)
    genomaSeparado.insert(int(i), g)
    return ''.join(genomaSeparado)

def concatenar(g: str) -> str:
    return genoma + g

def remover(i:int, j:int) -> str:
    genomaSeparado: list = separaString(genoma, i, j)
    return ''.join([genomaSeparado[0], genomaSeparado[2]])

def transpor_e_reverter(i:int, j:int, k:int) -> str:
    genomaTransposto = transpor(i, j, k)
    return reverter(i, k, genomaTransposto)

def buscar(g: str) -> int:
    print(genoma.count(g))

def buscar_bidirecional(g: str) -> int:
    print(genoma.count(g) + genoma[::-1].count(g))

def mostrar() -> None:
    print(genoma)

executar: bool = True
while executar:
    operacao = input().split(' ')
    match operacao[0]:
        case "reverter":
            if verificaIndices(int(operacao[1]), regra = 3):
                genoma = reverter(int(operacao[1]), int(operacao[2]), genoma)
        case "transpor":
            if verificaIndices(int(operacao[1]), int(operacao[2]), 4):
                genoma = transpor(int(operacao[1]), int(operacao[2]), int(operacao[3]))
        case "combinar":
            genoma = combinar(operacao[1], int(operacao[2]))
        case "concatenar":
            genoma = concatenar(operacao[1])
        case "remover":
            if verificaIndices(int(operacao[1]), regra = 3):
                genoma = remover(int(operacao[1]), int(operacao[2]))
        case "transpor_e_reverter":
            genoma = transpor_e_reverter(int(operacao[1]), int(operacao[2]), int(operacao[3]))
        case "buscar":
            buscar(operacao[1])
        case "buscar_bidirecional":
            buscar_bidirecional(operacao[1])
        case "mostrar":
            mostrar()
        case "sair":
            executar = False
