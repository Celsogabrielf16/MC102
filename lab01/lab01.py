choice1 = input()
choice2 = input()
movie1 = "Interestelar"
movie2 = "Jornada nas Estrelas"
result = ''
 
if choice1 == choice2:
    result = "empate"
elif choice1 == "pedra" and (choice2 == "lagarto" or choice2 == "tesoura"):
    result = movie1
elif choice1 == "papel" and (choice2 == "pedra" or choice2 == "spock"):
    result = movie1
elif choice1 == "tesoura" and (choice2 == "papel" or choice2 == "lagarto"):
    result = movie1
elif choice1 == "lagarto" and (choice2 == "spock" or choice2 == "papel"):
    result = movie1
elif choice1 == "spock" and (choice2 == "pedra" or choice2 == "tesoura"):
    result = movie1
elif choice2 == "pedra" and (choice1 == "lagarto" or choice1 == "tesoura"):
    result = movie2
elif choice2 == "papel" and (choice1 == "pedra" or choice1 == "spock"):
    result = movie2
elif choice2 == "tesoura" and (choice1 == "papel" or choice1 == "lagarto"):
    result = movie2
elif choice2 == "lagarto" and (choice1 == "spock" or choice1 == "papel"):
    result = movie2
elif choice2 == "spock" and (choice1 == "pedra" or choice1 == "tesoura"):
    result = movie2
else:
    result = "Jogada inexistente"
    
print(result)