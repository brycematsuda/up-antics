  # -*- coding: latin-1 -*-
import random
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import addCoords
from AIPlayerUtils import *
from Ant import *
from Location import *
from Building import *
from Inventory import *
from GameState import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Ryson / Bryce BFS")

    ##
    #getPlacement
    #Description: The getPlacement method corresponds to the
    #action taken on setup phase 1 and setup phase 2 of the game.
    #In setup phase 1, the AI player will be passed a copy of the
    #state as currentState which contains the board, accessed via
    #currentState.board. The player will then return a list of 10 tuple
    #coordinates (from their side of the board) that represent Locations
    #to place the anthill and 9 grass pieces. In setup phase 2, the player
    #will again be passed the state and needs to return a list of 2 tuple
    #coordinates (on their opponent�s side of the board) which represent
    #Locations to place the food sources. This is all that is necessary to
    #complete the setup phases.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is
    #       requesting a placement from the player.(GameState)
    #
    #Return: If setup phase 1: list of ten 2-tuples of ints -> [(x1,y1), (x2,y2),�,(x10,y10)]
    #       If setup phase 2: list of two 2-tuples of ints -> [(x1,y1), (x2,y2)]
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]

    ##
    #getMove
    #Description: The getMove method corresponds to the play phase of the game
    #and requests from the player a Move object. All types are symbolic
    #constants which can be referred to in Constants.py. The move object has a
    #field for type (moveType) as well as field for relevant coordinate
    #information (coordList). If for instance the player wishes to move an ant,
    #they simply return a Move object where the type field is the MOVE_ANT constant
    #and the coordList contains a listing of valid locations starting with an Ant
    #and containing only unoccupied spaces thereafter. A build is similar to a move
    #except the type is set as BUILD, a buildType is given, and a single coordinate
    #is in the list representing the build location. For an end turn, no coordinates
    #are necessary, just set the type as END and return.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is
    #       requesting a move from the player.(GameState)
    #
    #Return: Move(moveType [int], coordList [list of 2-tuples of ints], buildType [int]
    ##
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        movesRatings = []
        for move in moves:
            nextState = updateState(self,currentState, move)
            rating = evaluateState(self, nextState)
            nextInv = nextState.inventories[self.playerId]
            currInv = currentState.inventories[self.playerId]
            # Higher rating if food count or amount of carrying ants will go up next state
            # compared to previous state
            if nextInv.foodCount > currInv.foodCount or \
                countCarrying(nextInv.ants) > countCarrying(currInv.ants):
                rating += 0.25

            movesRatings.append((rating, move))

        sortedRatings = sorted(movesRatings, key=lambda x: x[0], reverse=True)
        bestMoveRating = sortedRatings[0]
        bestMove = bestMoveRating[1]
        return bestMove

    ##
    #getAttack
    #Description: The getAttack method is called on the player whenever an ant completes
    #a move and has a valid attack. It is assumed that an attack will always be made
    #because there is no strategic advantage from withholding an attack. The AIPlayer
    #is passed a copy of the state which again contains the board and also a clone of
    #the attacking ant. The player is also passed a list of coordinate tuples which
    #represent valid locations for attack. Hint: a random AI can simply return one of
    #these coordinates for a valid attack.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is requesting
    #       a move from the player. (GameState)
    #   attackingAnt - A clone of the ant currently making the attack. (Ant)
    #   enemyLocation - A list of coordinate locations for valid attacks (i.e.
    #       enemies within range) ([list of 2-tuples of ints])
    #
    #Return: A coordinate that matches one of the entries of enemyLocations. ((int,int))
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

##
#updatedState
#Description: Determines what the agent's state would look like after a given move
#
#Parameters:
#   currentState: the current state of the game
#   Move: a move object
#
#Return:
#   possibleState: A copy of currentState that has been altered to be a node
##
def updateState(self, currentState, move):
#Create a copy of the current state to make a state for a potential move
    stateCopy = currentState.fastclone()
    #Create a copy of the current player's inventory
    currInventory = getCurrPlayerInventory(stateCopy)
    #get a reference to where the enemy ants are
    enemyAntList = getAntList(stateCopy, self.playerId - 1, [(QUEEN, WORKER, DRONE, SOLDIER, R_SOLDIER)])
    #part a
    if(move.moveType == BUILD):
        antInitCoords = getConstrList(currentState, self.playerId, [(ANTHILL)])[0].coords
        newAnt = Ant(antInitCoords, move.buildType, self.playerId)
        currInventory.ants.append(newAnt)
        #part f
        if(newAnt.type == SOLDIER):
            currInventory.foodCount -= 3
        elif(newAnt.type == DRONE or newAnt.type == WORKER):
            currInventory.foodCount -= 1
        elif(newAnt.type == R_SOLDIER):
            currInventory.foodCount -= 2
    #part b
    if(move.moveType == MOVE_ANT):
        ant = getAntAt(stateCopy, move.coordList[0])
        newSpot = move.coordList[len(move.coordList) - 1]
        ant.coords = newSpot
        #part d
        adjacent = listAdjacent(ant.coords)
        for x in range(0, len(adjacent)):
            for y in range(0, len(enemyAntList)):
                if(adjacent[x] == enemyAntList[y].coords):
                    attackedAnt = getAntAt(stateCopy, adjacent[x])
                    attackedAnt.health -= 1
                    if(attackedAnt.health <= 0):
                        enemyAntList.remove(attackedAnt)
        #part c
        foodList = getConstrList(stateCopy, None, [(FOOD)])
        for food in foodList:
            if(ant.coords == food.coords and ant.carrying == False):
                ant.carrying = True
        if(ant.coords == getConstrList(stateCopy, self.playerId, [(ANTHILL)])[0].coords and ant.carrying == True):
            ant.carrying = False
            currInventory.foodCount += 1

    #part e
    return stateCopy


##
#evaluateState
#Description: evaluates a given state and assigns to it a rating
#
#Parameters:
#   currentState: the current state of the game
#
#Return:
#   rating: a rating (between 0.0 - 1.0) of the examined game state.
#           0.0 = Lose, 1.0 = Win, <0.5 = Losing, >=0.5 = Winning.
##
def evaluateState(self, currentState):
    oppId = 1 if self.playerId - 1 == -1 else 0
    enemyQueenAnt = getAntList(currentState, oppId, [(QUEEN)])

    friendlyWorkerAnts = getAntList(currentState, self.playerId, [(WORKER)])
    friendlyDroneAnts = getAntList(currentState, self.playerId, [(DRONE)])
    friendlySoldierAnts = getAntList(currentState, self.playerId, [(SOLDIER)])
    friendlyRangedAnts = getAntList(currentState, self.playerId, [(R_SOLDIER)])
    friendlyQueenAnt = getAntList(currentState, self.playerId, [(QUEEN)])[0]

    enemyInventory = currentState.inventories[self.playerId - 1]
    friendlyInventory = currentState.inventories[self.playerId]

    foodList = getConstrList(currentState, None, [(FOOD)])

    foodCoordList = []
    for food in foodList:
        foodCoordList.append(food.coords)

    friendlyConstrList = getConstrList(currentState, self.playerId, [(ANTHILL, TUNNEL)])
    tunnelList = getConstrList(currentState, self.playerId, [(TUNNEL)])
    constrCoordList = []
    for constr in friendlyConstrList:
        constrCoordList.append(constr.coords)

    # Win / lose cases
    if not enemyQueenAnt or friendlyInventory.foodCount >= 11:
        return 1.0
    elif not friendlyQueenAnt or enemyInventory.foodCount >= 11:
        return 0.0
    elif len(tunnelList) > 1 or \
        len(friendlyDroneAnts) > 0 or \
        len(friendlySoldierAnts) > 0 or \
        len(friendlyRangedAnts) > 0 or \
        len(friendlyWorkerAnts) > 2:
            return 0.0001 # Do not build anything aside from worker ants
    else:
        rating = 0.6
        workerRating = 0.0

        # Keep 2 worker ants on the field to collect food
        if (len(friendlyWorkerAnts) == 2):
            rating += 0.2

        # Keep queen off the anthill and food
        if (friendlyQueenAnt.coords in foodCoordList) or (friendlyQueenAnt.coords in constrCoordList):
            rating -= 0.3

        # Keep queen away from enemies
        for coord in listAdjacent(friendlyQueenAnt.coords):
            if getAntAt(currentState, coord) != None:
                adjAnt = getAntAt(currentState, coord)
                if adjAnt.player != self.playerId:
                    rating -= 0.08

        for ant in friendlyWorkerAnts:
            if ant.carrying:
                # Find the closest tunnel / anthill
                anthillDist = stepsToReach(currentState, ant.coords, friendlyInventory.getAnthill().coords)
                tunnelDist = stepsToReach(currentState, ant.coords, friendlyInventory.getTunnels()[0].coords)

                workerRating = anthillDist if anthillDist < tunnelDist else tunnelDist
    
                rating -= (float(workerRating) / 100)

                if ant.coords in foodCoordList:
                    rating -= 0.035

            elif not ant.carrying:
                # Find the closest food
                foodStepList = []
                for foodCoord in foodCoordList:
                    foodStepList.append(stepsToReach(currentState, ant.coords, foodCoord))
                workerRating = min(foodStepList)
                rating -= (float(workerRating) / 100)

                if ant.coords in constrCoordList:
                    rating -= 0.035

        if rating < 0: 
            rating = random.uniform(0.0, 0.01)
        elif rating > 1: 
            rating = random.uniform(0.8, 0.9)
        return rating

# Counts the number of ants carrying food in an ants array
def countCarrying(ants):
    num = 0
    for ant in ants:
        if ant.carrying:
            num += 1
    return num

# Unit Test #1 - ensure evaluateState ftn is working properly
board = [[Location((col, row)) for row in xrange(0,BOARD_LENGTH)] for col in xrange(0,BOARD_LENGTH)]

player1Queen = Ant((4, 0), QUEEN, PLAYER_ONE)
player1Worker = Ant((0, 3), WORKER, PLAYER_ONE)
player1Worker.carrying = True

player2Queen = Ant((2, 5), QUEEN, PLAYER_TWO)
player2Worker = Ant((4, 6), WORKER, PLAYER_TWO)

player1Ants = [player1Queen, player1Worker]
player2Ants = [player2Queen, player2Worker]

player1Anthill = Building((2, 0), ANTHILL, PLAYER_ONE)
player1Tunnel = Building((3, 0), TUNNEL, PLAYER_ONE)

player2Anthill = Building((2, 5), ANTHILL, PLAYER_TWO)
player2Tunnel = Building((4, 5), TUNNEL, PLAYER_TWO)

foodList = [ Construction((7, 4), FOOD), Construction((0, 3), FOOD), Construction((4, 5), FOOD), Construction((2, 1), FOOD)]

player1Inv = Inventory(PLAYER_ONE, player1Ants, [player1Anthill, player1Tunnel], 1)
player2Inv = Inventory(PLAYER_TWO, player2Ants, [player2Anthill, player2Tunnel], 1)
neutralInv = Inventory(NEUTRAL, [], [], 0)

for ant in player1Ants:
    board[ant.coords[0]][ant.coords[1]].ant = ant
for ant in player2Ants:
    board[ant.coords[0]][ant.coords[1]].ant = ant

for construct in player1Inv.constrs:
    board[construct.coords[0]][construct.coords[1]].constr = construct
for construct in player2Inv.constrs:
    board[construct.coords[0]][construct.coords[1]].constr = construct

for food in foodList:
    board[food.coords[0]][food.coords[1]].constr = food

state = GameState(board, [player1Inv, player2Inv, neutralInv], PLAY_PHASE, PLAYER_ONE)

testMove = Move(MOVE_ANT, [(0, 3), (1, 3), (2, 3)], None)
testAI = AIPlayer(PLAYER_ONE)
testNewState = updateState(testAI, state, testMove)

evaluateVal = evaluateState(testAI, testNewState)
if (evaluateVal == 0.57):
    print "Unit Test #1 Passed"
else:
    print "Unit Test #1 Failed. Got " + str(evaluateVal) + " instead of 0.57. Check the evaluateState function."
