dailyReport = []

analyzedDays = int(input())
for day in range(analyzedDays):
    couplesFight = []
    proceduresAvailable = []
    desiredProcedures = []
    animalsCaredFor = []
    carelessAnimals = []
    requestedProcedureNotAvailable = []
    fightCount = 0
    couplesFightNumber = int(input())
    for couple in range(1, couplesFightNumber + 1):
        couplesFight.append(input().split(" "))

    proceduresAvailable = input().split(" ")
    for amount in range(1, len(proceduresAvailable) + 1, 2):
        proceduresAvailable[amount] = int(proceduresAvailable[amount])

    animalsPresentNumber = int(input())
    for animalProcedure in range(animalsPresentNumber):
        desiredProcedures.append(input().split(" "))

    for fight in couplesFight:
        animal1 = animal2 = False
        for animalsPresent in desiredProcedures:
            if animalsPresent[0] == fight[0]:
                animal1 = True
            elif animalsPresent[0] == fight[1]:
                animal2 = True
        if animal1 and animal2:
            fightCount += 1

    for animalProcedure in desiredProcedures:
        procedureNotAvailable = True
        for i in range(0, len(proceduresAvailable), 2):
            indexAmount = proceduresAvailable.index(proceduresAvailable[i]) + 1
            if proceduresAvailable[indexAmount] != 0 and proceduresAvailable[i] == animalProcedure[1]:
                animalsCaredFor.append(animalProcedure[0])
                proceduresAvailable[indexAmount] -= 1
                procedureNotAvailable = False
            elif proceduresAvailable[i] == animalProcedure[1]:
                carelessAnimals.append(animalProcedure[0])
                procedureNotAvailable = False
        if procedureNotAvailable:
            requestedProcedureNotAvailable.append(animalProcedure[0])

    dailyReport.append([day + 1, fightCount, animalsCaredFor, carelessAnimals, requestedProcedureNotAvailable])

for day in dailyReport:
    print("Dia:", day[0])
    print("Brigas:", day[1])
    if len(day[2]) != 0:
        print("Animais atendidos:", end=" ")
        for item in day[2]:
            if len(day[2]) - 1 == day[2].index(item):
                print(item)
            else:
                print(item, end=", ")
    if len(day[3]) != 0:
        print("Animais não atendidos:", end=" ")
        for item in day[3]:
            if len(day[3]) - 1 == day[3].index(item):
                print(item)
            else:
                print(item, end=", ")
    if len(day[4]) != 0:
        for item in day[4]:
            print("Animal", item, "solicitou procedimento não disponível.")
    print()
