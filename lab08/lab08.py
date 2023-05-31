# Cria um dicionario com as chaves sendo o nome de cada categoria simples, e o valor sendo
# uma lista com o nome do filme, sua nota total e a quantidade de avaliações
def criaDicionarioCategorias(listaAvaliacoes: list) -> dict[str, list]:
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


# Define qual filme ganhou cada categoria simples
def determinaVencedoresCategoriasSimples(dicionarioCategorias: dict) -> dict[str, str]:
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


# Define qual filme ganhou a categoria de pior filme
def determinaVencedorPiorFilme(listaFilmesIndicados: list, vencedoresCategoriasSimples: dict, dicionarioCategorias: dict) -> str:
    numeroVitorias: list[int] = determinaNumeroDeVitorias(listaFilmesIndicados, vencedoresCategoriasSimples)
    if numeroVitorias.count(max(numeroVitorias)) == 1:
        return listaFilmesIndicados[numeroVitorias.index(max(numeroVitorias))]
    else:
        mediaSomadasFilmes = somaMedias(numeroVitorias, listaFilmesIndicados, dicionarioCategorias)
        return listaFilmesIndicados[mediaSomadasFilmes.index(max(mediaSomadasFilmes))]


# Cria uma lista com a quantidade de vitorias de cada filme
def determinaNumeroDeVitorias(listaFilmesIndicados: list, vencedoresCategoriasSimples: dict) -> list[int]:
    numeroVitorias: list[int] = []
    for filme in listaFilmesIndicados:
        numeroVitorias.append(0)
        for filmeVencedor in vencedoresCategoriasSimples.values():
            if filme == filmeVencedor:
                numeroVitorias[listaFilmesIndicados.index(filmeVencedor)] += 1
    return numeroVitorias


# Soma as medias das notas dos filmes em todas as categorias como criterio de desempate
def somaMedias(filmesQueVenceram: list[int], listaFilmesIndicados: list, dicionarioCategorias: dict) -> list[float]:
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


# Define o vencedor da categoria não merecia estar aqui
def determinaVencedorNaoMereciaEstarAqui(listaFilmesIndicados: list, dicionarioCategorias: dict) -> list[str]:
    filmesNaoAvaliados: list[str] = []
    for filme in listaFilmesIndicados:
        naoFoiAvaliado: bool = True
        for categoria in dicionarioCategorias.values():
            if categoria.count(filme) == 1:
                naoFoiAvaliado = False
        if naoFoiAvaliado:
            filmesNaoAvaliados.append(filme)
    return filmesNaoAvaliados


# Mostra os vencedores
def mostrar(vencedoresCategoriasSimples: dict, vencedorPiorFilme: str, vencedorNaoMereciaEstarAqui: list) -> None:
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


def main() -> None:
    numeroFilmesIndicados: int = int(input())
    listaFilmesIndicados: list[str] = []

    for _ in range(numeroFilmesIndicados):
        listaFilmesIndicados.append(input())

    numeroAvaliacoes: int = int(input())
    listaAvaliacoes: list[list[str]] = []

    for _ in range(numeroAvaliacoes):
        listaAvaliacoes.append(input().split(', '))

    dicionarioCategorias = criaDicionarioCategorias(listaAvaliacoes)
    vencedoresCategoriasSimples = determinaVencedoresCategoriasSimples(dicionarioCategorias)
    vencedorPiorFilme = determinaVencedorPiorFilme(listaFilmesIndicados, vencedoresCategoriasSimples, dicionarioCategorias)
    vencedorNaoMereciaEstarAqui = determinaVencedorNaoMereciaEstarAqui(listaFilmesIndicados, dicionarioCategorias)

    mostrar(vencedoresCategoriasSimples, vencedorPiorFilme, vencedorNaoMereciaEstarAqui)


if __name__ == '__main__':
    main()
