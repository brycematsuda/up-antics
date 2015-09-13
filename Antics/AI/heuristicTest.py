import random
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import addCoords
from AIPlayerUtils import *

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
        super(AIPlayer,self).__init__(inputPlayerId, "Heuristic AI Test")
    

    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        if currentState.phase == SETUP_PHASE_1:    # stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    if i == 0: # Placing anthill as far back as possible
                        x = random.randint(0, 9)
                        y = 0
                    elif i > 1: # Placing grass on edge of territory
                        y = 3
                        for j in range(0, 9):
                            move = (j, y)
                            if move not in moves: x = j
                    else: # Pick a random spot for tunnel for now (not on grass)
                        x = random.randint(0, 9)
                        y = random.randint(0, 2)

                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   # stuff on foe's side
            oppId = getOpponentId(self)
                
            oppConstr = getConstrList(currentState, oppId)
            oppAnthill = None
            if (oppConstr[0].type == TUNNEL):
                oppAnthill = oppConstr[0].coords
            else:
                oppAnthill = oppConstr[1].coords

            moves = []
            move = None
            tileDist = [] # List of tuples representing all distances from empty spaces to anthill
            for x in range(0, 10):
                for y in range(6, 10):
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        steps = stepsToReach(currentState, (x, y), oppAnthill)
                        coord = (x, y)
                        tileDist.append((steps, coord))

            # http://stackoverflow.com/a/3121985 -- sorts list from highest distance to lowest
            tileDist.sort(key=lambda tup: tup[0], reverse=True)

            # Place opponent's food in the farthest 2 distances from their anthill
            # (TODO: Find a better method. The farthest 2 distances could be the shortest two to the tunnel)
            farthestTile1 = tileDist[0]
            farthestCoord1 = farthestTile1[1]

            farthestTile2 = tileDist[1]
            farthestCoord2 = farthestTile2[1]
            
            moves.append(farthestCoord1)
            moves.append(farthestCoord2)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        oppId = getOpponentId(self)
        moves = listAllLegalMoves(currentState)
        ants = getAntList(currentState, self.playerId)
        enemyQueen = getAntList(currentState, oppId, [(QUEEN)])[0].coords
        constrList = getConstrList(currentState, None)
        foodList = []
        storageList = []
        hillTunnelList = getConstrList(currentState, self.playerId, [ANTHILL, TUNNEL])
        anthill = getConstrList(currentState, self.playerId, [(ANTHILL)])[0].coords
        enemyAnthill = getConstrList(currentState, oppId, [(ANTHILL)])[0].coords
        buildMoves = listAllBuildMoves(currentState)

        # for move in buildMoves:
            # print move
        # for move in moves:
        #     print str(move)

        
        if buildMoves:
            # have at least 2 worker ants to grab from 2 food sources
            if (numAnts(self, currentState, WORKER) < 2):
                return buildMoves[0]
            # have at least 3 soldier ants to attack enemy base/queen
            if (numAnts(self, currentState, SOLDIER) < 3 and len(buildMoves) > 3):
                return buildMoves[2]

        for constr in constrList:
            # Make sure construction isn't already occupied by another ant
            if getAntAt(currentState, constr.coords) == None and (constr.type == FOOD):
                foodList.append(constr.coords)

        for hillTunnel in hillTunnelList:
            if (getAntAt(currentState, hillTunnel.coords) == None):
                storageList.append(hillTunnel.coords)

        for ant in ants:
            if ant.hasMoved: continue
            antMoveList = getAntMoveList(ant, moves)
            if ant.type != WORKER:
                if ant.type == QUEEN:
                    if (ant.coords == anthill or ant.coords in storageList or ant.coords in foodList): 
                        return antMoveList[random.randint(0, len(antMoveList) - 2)]

                    for coord in listAdjacent(ant.coords):
                        if getAntAt(currentState, coord) != None:
                         # Trust no ant.
                            return antMoveList[random.randint(0, len(antMoveList) - 2)]
                elif ant.type == SOLDIER:
                    if ant.coords == enemyAnthill:
                        return moves[len(moves) - 1] # start capturing the base

                    stepsToQueen = stepsToReach(currentState, ant.coords, enemyQueen)
                    stepsToAnthill = stepsToReach(currentState, ant.coords, enemyAnthill)

                    # If queen is closer, focus attack on her.
                    if (stepsToQueen < stepsToAnthill):
                        return getOptimalMove(currentState, enemyQueen, antMoveList)
                    else:
                        return getOptimalMove(currentState, enemyAnthill, antMoveList)
            else:
                bestMove = moves[len(moves) - 1] # default best move: do nothing
                for move in antMoveList:
                    # print str(move)
                    for coord in move.coordList:
                        # If worker ant is near food source and not carrying food, get food.
                        # If worker ant is near anthill or tunnel and carrying food, go drop it off.
                        if ant.coords in move.coordList:
                            if ((coord in foodList and getAntAt(currentState, constr.coords) == None and not ant.carrying) or (coord in storageList and getAntAt(currentState, constr.coords) == None and ant.carrying)):
                                bestMove = move
                            elif not ant.carrying:
                                closestFoodCoord = getClosestCoordInList(currentState, ant.coords, foodList)
                                bestMove = getOptimalMove(currentState, closestFoodCoord, antMoveList)
                            elif ant.carrying:
                                closestStorageCoord = getClosestCoordInList(currentState, ant.coords, storageList)
                                bestMove = getOptimalMove(currentState, closestStorageCoord, antMoveList)
                return bestMove
        return moves[len(moves) - 1] # if all ants have moved, end thy turn
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        # Kill everyone in sight.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]
 
def getClosestCoordInList(currentState, src, defList, reverse = False):
    if not defList: return src

    closest = []
    for dest in defList:
        steps = stepsToReach(currentState, src, dest)
        closest.append((steps, dest))

    if (reverse):
        closest.sort(key=lambda tup: tup[0], reverse=True)
    else:
        closest.sort(key=lambda tup: tup[0])

    closestTile = closest[0]
    closestCoord = closestTile[1]

    return closestCoord

def getOptimalMove(currentState, dest, antMoveList):
    bestOptMove = Move(MOVE_ANT, [antMoveList[0].coordList[0]], None) # default best move: staying in place
    for move in antMoveList:
        bestOptSteps = stepsToReach(currentState, bestOptMove.coordList[-1], dest)
        currMoveSteps = stepsToReach(currentState, move.coordList[-1], dest)
        if currMoveSteps < bestOptSteps: # we've found a better move that takes less steps
            bestOptMove = move
    return bestOptMove

def getAntMoveList(ant, moves):
    antMoveList = []
    for move in moves:
        if move.moveType != END and ant.coords == move.coordList[0]:
            antMoveList.append(move)
    return antMoveList

def numAnts(self, currentState, antType):
    ants = getAntList(currentState, self.playerId)
    num = 0
    for ant in ants:
        if (ant.type == antType):
            num += 1
    return num

def getOpponentId(self):
    oppId = PLAYER_TWO

    # Get opponent's anthill coordinates
    if (self.playerId == PLAYER_TWO):
        oppId = PLAYER_ONE

    return oppId