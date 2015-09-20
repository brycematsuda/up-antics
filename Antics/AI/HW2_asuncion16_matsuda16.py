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
            s = updateState(self,currentState, move)
            rating = evaluateState(self, s)
            movesRatings.append((rating, move))

        sortedRatings = sorted(movesRatings, key=lambda x: x[0], reverse=True)
        print sortedRatings[0]
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
    #Create a reference to all types of enemy ants
    enemyWorkerAnts = getAntList(currentState, self.playerId - 1, [(WORKER)])
    enemyDroneAnts = getAntList(currentState, self.playerId - 1, [(DRONE)])
    enemySoldierAnts = getAntList(currentState, self.playerId - 1, [(SOLDIER)])
    enemyRangedAnts = getAntList(currentState, self.playerId - 1, [(R_SOLDIER)])
    enemyQueenAnt = getAntList(currentState, self.playerId - 1, [(QUEEN)])

    #Create a reference to all types of friendly ants
    friendlyWorkerAnts = getAntList(currentState, self.playerId, [(WORKER)])
    friendlyDroneAnts = getAntList(currentState, self.playerId, [(DRONE)])
    friendlySoldierAnts = getAntList(currentState, self.playerId, [(SOLDIER)])
    friendlyRangedAnts = getAntList(currentState, self.playerId, [(R_SOLDIER)])
    friendlyQueenAnt = getAntList(currentState, self.playerId, [(QUEEN)])[0]

    #Create a copy of the current player's inventory and the enemy's inventory
    enemyInventory = currentState.inventories[self.playerId - 1]
    friendlyInventory = currentState.inventories[self.playerId]

    #Create a referece to all food on the board
    foodList = getConstrList(currentState, None, [(FOOD)])

    #Create a reference to the life of the enemy's anthill and current players anthill
    enemyHillLife = enemyInventory.getAnthill().captureHealth
    friendlyHillLife = friendlyInventory.getAnthill().captureHealth

    if not enemyQueenAnt or friendlyInventory.foodCount >= 11:
        return 1.0
    elif not friendlyQueenAnt or enemyInventory.foodCount >= 11:
        return 0.0
    else:
        rating = random.uniform(0.6, 0.8)
        foodVar = random.uniform(0.3, 0.4) if (friendlyInventory.foodCount > 3) else 0
        # carryingVar = -0.2 if (countCarrying(friendlyWorkerAnts) < countCarrying(enemyWorkerAnts)) else 0
        workerVar = random.uniform(0.2, 0.3) if (len(friendlyWorkerAnts) == len(enemyWorkerAnts)) else 0 
        queenHealthVar = random.uniform(0.6, 0.8) if (friendlyQueenAnt.health < 3) else 0
        queenInDangerVar = random.uniform(0.3, 0.5) if enemyInRangeOf(friendlyQueenAnt, self.playerId, currentState) else 0
        onlyQueen = random.uniform(0.8, 0.9) if (len(friendlyInventory.ants) == 1 and friendlyQueenAnt) else 0
        # hillVar = -0.3 if (friendlyHillLife < enemyHillLife) else 0
        rating -= (((queenHealthVar + queenInDangerVar + onlyQueen) / 2.0) + foodVar + workerVar)
        
        if rating < 0: 
            rating = random.uniform(0.1, 0.2)
        elif rating > 1: 
            rating = random.uniform(0.9, 1.0)
        return rating

def countCarrying(ants):
    num = 0
    for ant in ants:
        if ant.carrying:
            num += 1
    return num

def goodBadValue(num, testPass):
    if testPass:
        return num
    else:
        return -num

def enemyInRangeOf(ant, pid, currentState):
    for a in listAdjacent(ant.coords):
        if getAntAt(currentState, a):
            adjAnt = getAntAt(currentState, a)
            if (adjAnt.player != pid):
                return True
    return False