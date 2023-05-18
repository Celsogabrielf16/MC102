print("Este é um sistema que irá te ajudar a escolher a sua próxima Distribuição Linux. Responda a algumas poucas perguntas para ter uma recomendação.")
 
print("Seu SO anterior era Linux?")
print("(0) Não")
print("(1) Sim")
response1 = int(input())
 
if response1 == 0 or response1 == 1:
    if response1 == 0:
        print("Seu SO anterior era um MacOS?")
        print("(0) Não")
        print("(1) Sim")
        response2 = int(input())
 
        if response2 == 0 or response2 == 1:
            if response2 == 0:
                print("Você passará pelo caminho daqueles que decidiram abandonar sua zona de conforto, as distribuições recomendadas são: Ubuntu Mate, Ubuntu Mint, Kubuntu, Manjaro.")
            else:
                print("Você passará pelo caminho daqueles que decidiram abandonar sua zona de conforto, as distribuições recomendadas são: ElementaryOS, ApricityOS.")
        else:
            print("Opção inválida, recomece o questionário.")
 
    else:
        print("É programador/ desenvolvedor ou de áreas semelhantes?")
        print("(0) Não")
        print("(1) Sim")
        print("(2) Sim, realizo testes e invasão de sistemas")
        response2 = int(input())
 
        if response2 == 0 or response2 == 1 or response2 == 2:
            if response2 == 0:
                print("Ao trilhar esse caminho, um novo guru do Linux irá surgir, as distribuições que servirão de base para seu aprendizado são: Ubuntu Mint, Fedora.")
            elif response2 == 1:
                print("Gostaria de algo pronto para uso ao invés de ficar configurando o SO?")
                print("(0) Não")
                print("(1) Sim")
                response3 = int(input())
 
                if response3 == 0 or response3 == 1:
                    if response3 == 0:
                        print("Já utilizou Arch Linux?")
                        print("(0) Não")
                        print("(1) Sim")
                        response4 = int(input())
 
                        if response4 == 0 or response4 == 1:
                            if response4 == 0:
                                print("Ao trilhar esse caminho, um novo guru do Linux irá surgir, as distribuições que servirão de base para seu aprendizado são: Antergos, Arch Linux.")
                            else:
                                print("Suas escolhas te levaram a um caminho repleto de desafios, para você recomendamos as distribuições: Gentoo, CentOS, Slackware.")
                        else:
                            print("Opção inválida, recomece o questionário.")
                    else:
                        print("Já utilizou Debian ou Ubuntu?")
                        print("(0) Não")
                        print("(1) Sim")
                        response4 = int(input())
 
                        if response4 == 0 or response4 == 1:
                            if response4 == 0:
                                print("Ao trilhar esse caminho, um novo guru do Linux irá surgir, as distribuições que servirão de base para seu aprendizado são: OpenSuse, Ubuntu Mint, Ubuntu Mate, Ubuntu.")
                            else:
                                print("Suas escolhas te levaram a um caminho repleto de desafios, para você recomendamos as distribuições: Manjaro, ApricityOS.")
                        else:
                            print("Opção inválida, recomece o questionário.")
                else:
                    print("Opção inválida, recomece o questionário.")
            else:
                print("Ao trilhar esse caminho, um novo guru do Linux irá surgir, as distribuições que servirão de base para seu aprendizado são: Kali Linux, Black Arch.")
        else:
            print("Opção inválida, recomece o questionário.")
else:
    print("Opção inválida, recomece o questionário.")