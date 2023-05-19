numeroFilmesIndicados: int = int(input())
listaFilmesIndicados: list[str] = []

for _ in range(numeroFilmesIndicados):
    listaFilmesIndicados.append(input())

numeroAvaliacoes: int = int(input())
listaAvaliacoes: list[list[str]] = []

for _ in range(numeroAvaliacoes):
    listaAvaliacoes.append(input().split(', '))


def criaDicionarioCategorias() -> dict[str, list]:
    categorias: dict[str, list] = {
        'filme que causou mais bocejos': [],
        'filme que foi mais pausado': [],
        'filme que mais revirou olhos': [],
        'filme que não gerou discussão nas redes sociais': [],
        'enredo mais sem noção': []
    }

    for avaliacao in listaAvaliacoes:
        if categorias[avaliacao[1]].count(avaliacao[2]) == 0:
            categorias[avaliacao[1]].append(avaliacao[2])
            categorias[avaliacao[1]].append(int(avaliacao[3]))
            categorias[avaliacao[1]].append(1)
        else:
            indiceFilme = categorias[avaliacao[1]].index(avaliacao[2])
            notaAnterior = categorias[avaliacao[1]][indiceFilme + 1]
            categorias[avaliacao[1]][indiceFilme + 1] = notaAnterior + int(avaliacao[3])
            categorias[avaliacao[1]][indiceFilme + 2] += 1
    return categorias


def determinaVencedoresCategoriasSimples() -> dict[str, str]:
    vencedores = {}
    for chave, categoria in dicionarioCategorias.items():
        maiorNota: int = 0
        filmeMaiorNota: str = ''
        numeroAvaliacoes: int = 0
        for numeroAvaliacoesFilme in range(2, len(categoria), 3):
            if categoria[numeroAvaliacoesFilme] != 1:
                categoria[numeroAvaliacoesFilme - 1] /= categoria[numeroAvaliacoesFilme]
        for notaFilme in range(1, len(categoria), 3):
            if categoria[notaFilme] > maiorNota:
                maiorNota = categoria[notaFilme]
                filmeMaiorNota = categoria[notaFilme - 1]
                numeroAvaliacoes = categoria[notaFilme + 1]
            elif categoria[notaFilme] == maiorNota and categoria[notaFilme + 1] > numeroAvaliacoes:
                maiorNota = categoria[notaFilme]
                filmeMaiorNota = categoria[notaFilme - 1]
                numeroAvaliacoes = categoria[notaFilme + 1]
        vencedores[chave] = filmeMaiorNota
    return vencedores


def determinaVencedorPiorFilme() -> str:
    numeroVitorias: list[int] = determinaNumeroDeVitorias()
    if numeroVitorias.count(max(numeroVitorias)) == 1:
        return listaFilmesIndicados[numeroVitorias.index(max(numeroVitorias))]
    else:
        mediaSomadasFilmes = somaMedias(numeroVitorias)
        return listaFilmesIndicados[mediaSomadasFilmes.index(max(mediaSomadasFilmes))]


def determinaNumeroDeVitorias() -> list[int]:
    numeroVitorias: list[int] = []
    for filme in listaFilmesIndicados:
        numeroVitorias.append(0)
        for filmeVencedor in vencedoresCategoriasSimples.values():
            if filme == filmeVencedor:
                numeroVitorias[listaFilmesIndicados.index(filmeVencedor)] += 1
    return numeroVitorias


def somaMedias(filmesQueVenceram: list[int]) -> list[float]:
    indiceFilme: int = 0
    mediaSomadasFilmes: list[float] = []
    for filme in listaFilmesIndicados:
        mediaSomadasFilmes.append(0)
        for categoria in dicionarioCategorias.values():
            if categoria.count(filme) == 1 and filmesQueVenceram[indiceFilme] != 0:
                mediaSomadasFilmes[indiceFilme] += categoria[categoria.index(
                    filme) + 1]
        indiceFilme += 1
    return mediaSomadasFilmes


def determinaVencedorNaoMereciaEstarAqui() -> list[str]:
    filmesNaoAvaliados: list[str] = []
    for filme in listaFilmesIndicados:
        naoFoiAvaliado: bool = True
        for categoria in dicionarioCategorias.values():
            if categoria.count(filme) == 1:
                naoFoiAvaliado = False
        if naoFoiAvaliado:
            filmesNaoAvaliados.append(filme)
    return filmesNaoAvaliados


dicionarioCategorias = criaDicionarioCategorias()
vencedoresCategoriasSimples = determinaVencedoresCategoriasSimples()
vencedorPiorFilme = determinaVencedorPiorFilme()
vencedorNaoMereciaEstarAqui = determinaVencedorNaoMereciaEstarAqui()


def mostrar() -> None:
    print('#### abacaxi de ouro ####', end='\n\n')
    print('categorias simples')
    for chave, valor in vencedoresCategoriasSimples.items():
        print(f'categoria: {chave}')
        print(f'- {valor}')
    print()
    print('categorias especiais')
    print('prêmio pior filme do ano')
    print(f'- {vencedorPiorFilme}')
    print('prêmio não merecia estar aqui')
    if len(vencedorNaoMereciaEstarAqui) == 0:
        print('- sem ganhadores')
    else:
        print('-', end=' ')
        for i in range(len(vencedorNaoMereciaEstarAqui)):
            if i == len(vencedorNaoMereciaEstarAqui) - 1:
                print(vencedorNaoMereciaEstarAqui[i])
            else:
                print(vencedorNaoMereciaEstarAqui[i], end=", ")


mostrar()
