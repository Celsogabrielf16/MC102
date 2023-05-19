numberPlayers = int(input())
magicBoxNumber = input().split()
interval = input().split()
score = []
higherNumber = 0

i = 0
while i < numberPlayers:
    if (numberPlayers % 2 == 0 and (numberPlayers / 2) >= i + 1) or (numberPlayers % 2 == 1 and (numberPlayers // 2) >= i):
        scorePlayer = (int(interval[i * 2 + 1]) - int(interval[i * 2])) * int(magicBoxNumber[i])
    else:
        scorePlayer = (int(interval[i * 2 + 1]) - int(interval[i * 2])) + int(magicBoxNumber[i])
    score.append(scorePlayer)
    if scorePlayer > higherNumber:
      higherNumber = scorePlayer
    i += 1
if score.count(higherNumber) == 1:
    winner = score.index(higherNumber) + 1
    print("O jogador número", winner, "vai receber o melhor bolo da cidade pois venceu com", higherNumber, "ponto(s)!")
else:
    print("Rodada de cerveja para todos os jogadores!")