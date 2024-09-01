# a python baseball simulator based off of the dice game "Deadball"
# ver 0.1

import random

innings = 9
batters = 9
scoreHome = 0
scoreAway = 0
bases = [False, False, False]
lineupHome = []
lineupAway = []
pitcherHome = 0.00
pitcherAway = 0.00


#completed - gets the lineup and their batting averages (batter target)
def getLineup():
    lineup = []
    global batters
    for i in range(batters):
        ba = float(input("Batter " + str((i + 1)) + "'s batting average: "))
        lineup.append(round(ba, 2) * 100)
    return lineup

#completed - gets and returns the pitcher's ERA
def getPitcher():
    era = float(input("Pitcher's earned run average: "))
    return era

#completed - determines what die to use based off of the ERA 
def getPitchDie(era):
    if era >= 0 and era < 1.00:
        pitchDie = 20
    elif era >= 1.00 and era < 2.00:
        pitchDie = 12
    elif era >= 2.00 and era < 3.00:
        pitchDie = 8
    elif era >= 3.00 and era < 3.50:
        pitchDie = 4
    elif era >= 3.50 and era < 4.00:
        pitchDie = 4
    elif era >= 4.00 and era < 5.00:
        pitchDie = 8
    elif era >= 5.00 and era < 6.00:
        pitchDie = 12
    elif era >= 6.00 and era < 7.00:
        pitchDie = 20

    return pitchDie

#completed - finds out if at bat ended in a hit or out
def resolveAtBat(era, ba):
    if era < 7.00:
        die = getPitchDie(era)
    swingScore = random.randint(1, 100)
    
    if era < 3.50:
        dieRoll = random.randint(1, die)
        swingScore += dieRoll

    elif era >= 3.50 and era < 7.00:
        dieRoll = -1 * random.randint(1, die)
        swingScore += dieRoll
    
    elif era >= 7.00 and era < 8.00:
        swingScore -= 20
    
    elif era >= 8.00:
        swingScore -= 25
    
    #print(swingScore, ba, era)
    if swingScore <= ba:
        return "hit"

    else:
        return "out"
#completed - moves runners (not batter) and adds to score
def moveRunners(baseMove):
    global bases
    score = 0
    if baseMove == 1:
        # if runner on 3rd
        if bases[2]:
            bases[2] = False
            score += 1
        # if runner on 2nd
        if bases[1]:
            bases[1] = False
            bases[2] = True
        # if runner of 1st
        if bases[0]:
            bases[0] = False
            bases[1] = True
    
    elif baseMove == 2:
        if bases[2]:
            bases[2] = False
            score += 1
        if bases[1]:
            bases[1] = False
            score += 1
        if bases[0]:
            bases[0] = False
            bases[2] = True
    
    elif baseMove == 3:
        if bases[2]:
            score += 1
        if bases[1]:
            score += 1
        if bases[0]:
            score += 1

        for i in range(2):
            bases[i] = False
    return score

#completed - finds out what kind of hit the batter got
def findHit():
    die = random.randint(1, 20)

    if die >= 1 and die <= 12:
        return "single"
    elif die >= 13 and die <= 17:
        return "double"
    elif die == 18:
        return "triple"
    elif die == 19 or die == 20:
        return "hr"

def moveAllPlayers(hit):
    score = 0
    global bases
    if hit == "single":
        score += moveRunners(1)
        bases[0] = True
    elif hit == "double":
        score += moveRunners(2)
        bases[1] = True
    elif hit == "triple":
        score += moveRunners(3)
        bases[2] = True
    elif hit == "hr":
        for i in range(2):
            if bases[i]:
                score += 1
            bases[i] = False
        score += 1

    return score

def simInnings(lineup, score, pitcher, haPlayer):
    global bases
    outs = 0

    while outs < 3:
        result = resolveAtBat(pitcher, lineup[haPlayer])
        #print(result)
        if result == "out":
            outs += 1
            haPlayer += 1
            if haPlayer > 8:
                haPlayer = 0
            continue
        elif result == "hit":
            hit = findHit()
            #print(hit)
            score += moveAllPlayers(hit)
            #print(bases)
            haPlayer += 1
            if haPlayer > 8:
                haPlayer = 0
            continue
    
    for i in range(2):
        bases[i] = False
    #print(score)
    return haPlayer, score

def game():

    global bases
    scoreHome = 0
    playerHome = 0
    scoreAway = 0
    playerAway = 0
    awayWins = 0
    homeWins = 0
    n = int(input("How many times do you want to simulate the game? "))
    
    print("\nPlease input the stats as decimals Ex: 0.231 (batting average), 3.14 (earned run average)\n")
    print("Away team lineup?\n")
    lineupAway = getLineup()
    print("\nHome team lineup?\n")
    lineupHome = getLineup()
    
    print("\nAway team starting pitcher?\n")
    pitcherAway = getPitcher()
    print("\nHome team starting pitcher?\n")
    pitcherHome = getPitcher()
    
    resultsFile = open("prediction.txt", "w")
    #print("Home team:")
    print() 
    for j in range(n):
        for i in range(9):
            bases = [False, False, False]
            playerHome, scoreHome = simInnings(lineupHome, scoreHome, pitcherAway, playerHome)
            #print(scoreHome)
            #print("-" * 10)
        #print("Away team:")
        for i in range(9):
            bases = [False, False, False]
            playerAway, scoreAway = simInnings(lineupAway, scoreAway, pitcherHome, playerAway)
            #print(scoreAway)
            #print("-" * 10)
        print("Game " + str(j + 1) + ": "  + str(scoreAway) + " " + str(scoreHome))
        resultsFile.write("Game " + str(j + 1) + ": " + str(scoreAway) + " " + str(scoreHome) + "\n")
        if scoreAway > scoreHome:
            awayWins += 1
        elif scoreHome > scoreAway:
            homeWins += 1
        scoreHome, scoreAway = 0, 0
    print("\nThe scores were presented in the order of (away score, home score)")
    resultsFile.write("\nThe scores were presented in the order of (away score, home score)")
    print("\nAway team won " + str(awayWins) + " and home team won " + str(homeWins))
    resultsFile.write("\nAway team won " + str(awayWins) + " and home team won " + str(homeWins))
    resultsFile.close()

game()
